import os

from boj.core import http
from boj.core import constant
from boj.core import util
from boj.core.base import Command
from boj.core.error import IllegalStatementError
from boj.data.config import Config, FiletypeConfig
from boj.core.out import BojConsole
from boj.data.template_file import TemplateFile
from boj.data.testcase import Testcases
from boj.pages.boj_problem_page import BojProblemPage
from boj.data.boj_info import BojInfo


class AddCommand(Command):
    def execute(self, args):
        config = Config.load()

        console = BojConsole()
        with console.status("Checking for status..") as status:
            problem_dir = os.path.join(
                config.workspace.ongoing_dir,
                str(args.problem_id),
            )

            if not args.force and util.file_exists(
                os.path.join(problem_dir, ".boj-info.json")
            ):
                raise IllegalStatementError(f"Problem {args.problem_id} already exists")

            # Get language config
            filetype_config: FiletypeConfig = config.of_filetype(args.filetype)
            source_dir = config.get_source_dir(
                problem_id=args.problem_id,
                filetype=args.filetype,
            )
            os.makedirs(source_dir, exist_ok=True)

            # Get HTML content of given problem id from BOJ
            status.update("Crawling testcases..")
            problem_page = BojProblemPage.request(args.problem_id)

            # Create testcase file
            toml_testcase = Testcases(problem_page.find_testcases())
            toml_testcase.save(dir_=source_dir)

            # Create manifest files
            status.update("Creating resources..")
            if filetype_config.manifest_files:
                for f in filetype_config.manifest_files:
                    try:
                        manifest = TemplateFile.read_file(
                            path=os.path.join(config.workspace.template_dir, f)
                        )
                        manifest.save(path=os.path.join(problem_dir, f))
                    except (Exception,) as e:
                        console.log(e)

            # Create template file
            file_path = os.path.join(source_dir, filetype_config.filename)
            try:
                template_file_path = os.path.join(
                    config.workspace.template_dir,
                    f"template.{args.filetype}",
                )
                template = TemplateFile.read_file(path=template_file_path)
                template.save(path=file_path)
            except (FileNotFoundError,) as e:
                console.log(e)
                util.write_file(file_path, bytes("", "utf-8"))

            # Create BojInfo
            boj_info = BojInfo(
                root_dir=problem_dir,
                id_=args.problem_id,
                title=problem_page.find_title(),
                filetype=args.filetype,
                language=filetype_config.language,
                source_path=file_path.replace(problem_dir + os.sep, ""),
                testcase_path="testcase.toml",
                checksum=util.file_hash(file_path),
                accepted=False,
            )
            boj_info.save()
            console.print(f"Successfully initialized the problem {args.problem_id}")
