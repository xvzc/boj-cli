from rich.console import Console
from rich.markdown import Markdown
from boj.commands.problem import crawler as crawler

def run(args):
    html = crawler.query_problem(args.id)
    md = crawler.markdownify_problem(html, args.id)
    console = Console(width=85)
    console.print(Markdown(md))

