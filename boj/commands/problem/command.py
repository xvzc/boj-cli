from boj.core import util
import webbrowser

from boj.core.console import BojConsole


def execute(args):
    console = BojConsole()
    with console.status("Opening in browser..."):
        webbrowser.open(util.problem_url(args.id))

