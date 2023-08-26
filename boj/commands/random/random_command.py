import random
import webbrowser

import boj.core.auth
import boj.core.property
from boj.api.search import SolvedAcSearchApi
from boj.core import property
from boj.core.base import Command
from boj.core.error import IllegalStatementError
from boj.core.out import BojConsole


class RandomCommand(Command):
    def execute(self, args):
        console = BojConsole()
        with console.status("Reading credential...") as status:
            credential = boj.core.auth.read_credential()
            api = SolvedAcSearchApi(
                url=property.solved_ac_search_problem_url(),
                tags=args.tags,
                lang="ko",
                tier=args.tier,
                user=credential.username
            )

            status.update("Calling solved.ac API...")

            json = api.request().json()
            if not json or ('items' not in json):
                raise IllegalStatementError("Error while calling solve.ac API.")

            if len(json['items']) == 0:
                raise IllegalStatementError("No matching open found.")

            random_problem = random.choice(json['items'])

            status.update("Opening in browser...")
            webbrowser.open(boj.core.property.boj_problem_url(random_problem['problemId']))
