import time

import boj.core.util as util
from boj.commands.run.runner import CodeRunner
from boj.core.base import Command
from boj.core.config import Config
from boj.core.out import BojConsole


class RunCommand(Command):
    def execute(self, args, config: Config):
        console = BojConsole()

        with console.status("Loading source file...") as status:
            solution = util.read_solution(args.file)
            time.sleep(0.7)

            status.update("Loading testcases...")
            testcases = util.read_testcases()
            time.sleep(0.7)

        code_runner = CodeRunner(
            file_path=args.file,
            runner_config=config.filetype_config_of(solution.filetype),
            verbose=args.verbose or config.command.run.verbose,
            testcases=testcases,
        )

        code_runner.run_compile()  # Run if code_runner.compile != None
        code_runner.run_testcases()
