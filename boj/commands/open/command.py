import dataclasses
import webbrowser

from rich.console import Console

import boj.core.constant
from boj.core.command import Command
from boj.core.console import BojConsole
from boj.core.fs.file_search_strategy import UpwardSearchStrategy
from boj.data.boj_info import BojInfo, BojInfoRepository


@dataclasses.dataclass
class OpenCommand(Command):
    console: Console
    boj_info_repository: BojInfoRepository

    def execute(self, args):
        console = BojConsole()
        with console.status("Opening in browser..."):
            if args.problem_id:
                problem_id = args.problem_id
            else:
                self.boj_info_repository.search_strategy = UpwardSearchStrategy()
                boj_info = self.boj_info_repository.find(query=".boj-info.json")
                problem_id = boj_info.id

            webbrowser.open(boj.core.constant.boj_problem_url(problem_id))
