import dataclasses
import os

from rich.console import Console

from boj.commands.run.runner import CodeRunner
from boj.core.command import Command
from boj.core.fs.file_object import TextFile
from boj.core.fs.file_search_strategy import StaticSearchStrategy, UpwardSearchStrategy
from boj.core.fs.repository import ReadOnlyRepository, Repository
from boj.data.config import Config
from boj.data.boj_info import BojInfo
from boj.data.testcase import Testcase


@dataclasses.dataclass
class RunCommand(Command):
    console: Console
    config_repository: ReadOnlyRepository[Config]
    boj_info_repository: Repository[BojInfo]
    text_file_repository: Repository[TextFile]

    def read_testcase(self, testcase_dir, id_):
        return Testcase.of(
            label=id_,
            input_=self.text_file_repository.find(
                cwd=testcase_dir,
                query=os.path.join(id_, "input.txt"),
            ),
            output=self.text_file_repository.find(
                cwd=testcase_dir,
                query=os.path.join(id_, "output.txt"),
            ),
        )

    def execute(self, args):
        config = self.config_repository.find()
        with self.console.status("Loading config...") as status:
            status.update("Looking for problem information...")
            self.boj_info_repository.search_strategy = (
                StaticSearchStrategy() if args.problem_id else UpwardSearchStrategy()
            )
            cwd = config.workspace.search_dir(args.problem_id)
            boj_info = self.boj_info_repository.find(cwd, ".boj-info.json")

            status.update("Loading testcases...")
            testcases: list[Testcase] = []
            testcase_dir = boj_info.testcase_dir(True)
            for id_ in sorted(os.listdir(testcase_dir)):
                testcases.append(self.read_testcase(testcase_dir, id_))

            code_runner = CodeRunner(
                console=self.console,
                boj_info=boj_info,
                config=config.filetype(boj_info.filetype),
                timeout=args.timeout,
                testcases=testcases,
            )

            status.update("Compiling..")
            code_runner.run_compile()  # Run if code_runner.compile != None

        code_runner.run_testcases()
        code_runner.post_run()
