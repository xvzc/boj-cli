import boj.core.property
import webbrowser

from boj.core.base import Command
from boj.core.out import BojConsole


class OpenCommand(Command):
    def execute(self, args):
        console = BojConsole()
        with console.status("Opening in browser..."):
            webbrowser.open(boj.core.property.boj_problem_url(args.id))

