from rich.console import Console
from rich.markdown import Markdown
from boj.commands.problem import crawler as crawler

def run(args):
    md = crawler.query_problem(args.id)
    console = Console(width=85)
    console.print(Markdown(md))

