import webbrowser

import boj.core.constant
from boj.core.base import Command
from boj.core.config import Config
from boj.core.out import BojConsole


class OpenCommand(Command):
    def execute(self, args, config: Config):
        console = BojConsole()
        with console.status("Opening in browser..."):
            webbrowser.open(boj.core.constant.boj_problem_url(args.problem_id))
