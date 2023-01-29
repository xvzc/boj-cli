from boj.commands.init import crawler
from boj.core import util
import time

from boj.core.console import BojConsole


def execute(args):
    console = BojConsole()
    with console.status("Creating testcases...") as status:
        time.sleep(0.5)
        html = crawler.query_problem(args.problem_id)
        testcases = crawler.extract_testcases(html)
        yaml_testcases = crawler.yamlify_testcases(testcases)

        util.write_file('./testcase.yaml', yaml_testcases, 'w')
        console.print("Testcases have been created.")
