import time

from boj.commands.run.runner import CodeRunner
import boj.core.util as util
from boj.core.base import Command

from boj.core.out import BojConsole


class RunCommand(Command):
    def execute(self, args):
        console = BojConsole()

        with console.status("Loading source file...") as status:
            solution = util.read_solution(args.file)
            time.sleep(0.7)

            status.update("Loading configuration...")
            runner_config = util.read_runner_config(solution.filetype)
            time.sleep(0.7)

            status.update("Loading testcases...")
            testcases = util.read_testcases()
            time.sleep(0.7)

        code_runner = CodeRunner(
            file_path=args.file,
            runner_config=runner_config,
            verbose=args.verbose,
            testcases=testcases
        )

        code_runner.run_compile()  # Run if code_runner.compile != None
        code_runner.run_testcases()
