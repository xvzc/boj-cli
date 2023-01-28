from rich.console import Console
from boj.commands.problem.crawler import query_problem
from boj.commands.init import crawler
from boj.core import util

def run(args):
    console = Console()
    with console.status(
        "[bold yellow]Creating testcases...",
        spinner_style="white",
    ) as status:
        html = query_problem(args.problem_id)
        testcases = crawler.extract_testcases(html)
        yaml_testcases = crawler.yamlify_testcases(testcases)

        util.write_file('./testcase.yaml', yaml_testcases, 'w')
