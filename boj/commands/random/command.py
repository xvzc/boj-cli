import random
import webbrowser

from boj.core import util
from boj.core.console import BojConsole
from boj.commands.random import crawler as random_crawler


def execute(args):
    console = BojConsole()
    with console.status("Reading credential...") as status:
        credential = util.read_credential()
        if not credential:
            console.print_err("Login required")
            exit(1)

        level = None
        if args.normal:
            level = "hard"

        if args.normal:
            level = "normal"

        if args.easy:
            level = "easy"

        user = credential["user"]
        params = random_crawler.create_problem_query(user, args.tier, level)

        status.update("Calling solved.ac API...")

        problems = random_crawler.query_random_problems(params)
        if not problems or 'items' not in problems:
            console.print_err("And error while calling solved.ac API")
            exit(1)

        random_problem = random.choice(problems['items'])

        status.update("Opening in browser...")
        webbrowser.open(util.problem_url(random_problem['problemId']))
