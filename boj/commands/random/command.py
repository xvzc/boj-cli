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

        user = credential["user"]
        params = random_crawler.create_problem_query(user, args.tier, args.tags)

        status.update("Calling solved.ac API...")

        response = random_crawler.query_random_problems(params)
        if not response or ('items' not in response) or not response["items"]:
            console.print_err("Error while calling solved.ac API")
            exit(1)

        random_problem = random.choice(response['items'])

        status.update("Opening in browser...")
        webbrowser.open(util.problem_url(random_problem['problemId']))
