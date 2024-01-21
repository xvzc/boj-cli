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
            config = Config.load()

            status.update("Looking for problem information...")

            boj_info = BojInfo.find_any(
                ongoing_dir=config.workspace.ongoing_dir,
                problem_id=args.problem_id
            )

            status.update("Loading source file...")
            solution = Solution.read(boj_info)

            status.update("Loading testcases...")

            code_runner = CodeRunner(
                console=console,
                file_path=solution.path,
                ft_config=config.of_filetype(boj_info.filetype),
                timeout=args.timeout,
                testcases=TomlTestcase.read(boj_info.get_testcase_path()),
            )

            status.update("Compiling..")
            code_runner.run_compile()  # Run if code_runner.compile != None

        code_runner.run_testcases()
        code_runner.post_run()
