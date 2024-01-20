import time

from boj.commands.run.runner import CodeRunner
from boj.core.base import Command
from boj.core.config import Config
from boj.core.out import BojConsole
from boj.data.boj_info import BojInfo
from boj.data.solution import Solution
from boj.data.testcase import TomlTestcase


class RunCommand(Command):
    def execute(self, args):
        console = BojConsole()
        with console.status("Loading config...") as status:
            time.sleep(0.26)
            config = Config.load()

            status.update("Looking for problem information...")
            time.sleep(0.29)

            boj_info = BojInfo.find_any(
                problem_dir=config.workspace.problem_dir,
                problem_id=args.problem_id
            )
            console.log("Successfully loaded configuration")

        with console.status("Loading source file...") as status:
            solution = Solution.read(boj_info)
            time.sleep(0.21)

            status.update("Loading testcases...")
            time.sleep(0.22)

        code_runner = CodeRunner(
            file_path=solution.path,
            ft_config=config.of_filetype(boj_info.filetype),
            timeout=args.timeout,
            testcases=TomlTestcase.read(boj_info.get_testcase_path()),
        )

        code_runner.run_compile()  # Run if code_runner.compile != None
        code_runner.run_testcases()
        code_runner.post_run()
