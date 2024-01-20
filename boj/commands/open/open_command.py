import webbrowser

import boj.core.constant
from boj.core.base import Command
from boj.core.out import BojConsole
from boj.core.config import Config
from boj.data.boj_info import BojInfo


class OpenCommand(Command):
    def execute(self, args):
        console = BojConsole()
        with console.status("Opening in browser..."):
            problem_id = None
            if args.problem_id:
                problem_id = args.problem_id
            else:
                config = Config.load()
                boj_info = BojInfo.find_any(
                    problem_dir=config.workspace.problem_dir,
                    problem_id=None
                )
                problem_id = boj_info.id

            webbrowser.open(boj.core.constant.boj_problem_url(problem_id))
