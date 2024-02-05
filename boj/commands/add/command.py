import dataclasses
import os

from rich.console import Console

from boj.core import http
from boj.core.command import Command
from boj.core.error import IllegalStatementError, ResourceNotFoundError
from boj.core.fs.repository import Repository, ReadOnlyRepository
from boj.core.fs.file_object import TextFile
from boj.core.html import HtmlParser
from boj.core.http import HtmlResponse
from boj.core.fs.util import file_exists
from boj.data.config import Config
from boj.data.testcase import Testcase
from boj.web.boj_problem_page import (
    BojProblemPageRequest,
)
from boj.data.boj_info import BojInfo


@dataclasses.dataclass
class AddCommand(Command):
    console: Console
    config_repository: ReadOnlyRepository[Config]
    boj_info_repository: Repository[BojInfo]
    text_file_repository: Repository[TextFile]
    title_parser: HtmlParser[str]
    testcase_parser: HtmlParser[list[Testcase]]

    def execute(self, args):
        config = self.config_repository.find()

        with self.console.status("Checking for status..") as status:
            filetype = args.filetype or config.general.default_filetype
            if not filetype:
                message = "missing required argument '--type' or 'config.general.default_filetype'"
                raise IllegalStatementError(message)

            # Get HTML content of given problem id from BOJ
            status.update("Crawling testcases..")
            problem_page = HtmlResponse(
                http.get(BojProblemPageRequest(args.problem_id))
            )

            problem_title = self.title_parser.find(problem_page.html)
            boj_info: BojInfo = BojInfo.of(
                id_=args.problem_id,
                title=problem_title,
                config=config.filetype(filetype),
                dir_=config.workspace.problem_dir(args.problem_id),
            )

            if not args.force and file_exists(boj_info.metadata.path):
                raise IllegalStatementError(f"Problem {args.problem_id} already exists")

            # Create testcases
            # os.makedirs(boj_info.source_dir, exist_ok=True)
            testcases = self.testcase_parser.find(problem_page.html)
            for testcase in testcases:
                input_, output = testcase.to_text_files(boj_info.testcase_dir(True))
                self.text_file_repository.save(input_)
                self.text_file_repository.save(output)

            # Create manifest files
            status.update("Creating root templates..")
            self.populate_template_files(
                filenames=config.filetype(filetype).root_templates,
                src_dir=config.workspace.template_dir(abs_=True),
                dest_dir=boj_info.metadata.dir,
            )

            status.update("Creating source templates..")
            self.populate_template_files(
                filenames=config.filetype(filetype).source_templates,
                src_dir=config.workspace.template_dir(abs_=True),
                dest_dir=boj_info.source_dir,
            )

            source_code = self.text_file_repository.find(
                query=boj_info.source_path(abs_=False),
                cwd=config.workspace.problem_dir(args.problem_id),
            )
            boj_info.checksum = self.text_file_repository.hash(source_code)

            self.boj_info_repository.save(boj_info)
            self.console.log(f"Successfully added the problem {args.problem_id}")

    def populate_template_files(
        self,
        filenames: list[str],
        src_dir: str,
        dest_dir: str,
    ):
        for filename in filenames:
            try:
                file = self.text_file_repository.find(query=filename, cwd=src_dir)
                self.text_file_repository.copy(
                    obj=file,
                    dest=os.path.join(dest_dir, filename),
                )
            except ResourceNotFoundError as e:
                self.console.log(f"Skipped '{filename}' since it doesn't exist.")
