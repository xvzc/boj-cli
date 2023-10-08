import random
import webbrowser

import boj.core.auth
import boj.core.constant
from boj.core import constant
from boj.core.base import Command
from boj.core.config import Config, RandomOption
from boj.core.error import IllegalStatementError
from boj.core.out import BojConsole
from boj.api.solved_ac_search_api import SolvedAcSearchApi, SolvedAcSearchApiParam


class RandomCommand(Command):
    def execute(self, args, config: Config):
        console = BojConsole()
        with console.status("Reading credential...") as status:
            credential = boj.core.auth.read_credential()
            api = SolvedAcSearchApi(
                url=constant.solved_ac_search_problem_url(),
                param=SolvedAcSearchApiParam(
                    tags=args.tags or config.command.random.tags,
                    lang="ko",
                    tier=args.tier or config.command.random.tier,
                    user=credential.username,
                ),
            )

            status.update("Calling solved.ac API...")

            json = api.request().json()
            if not json or ("items" not in json):
                raise IllegalStatementError("Error while calling solve.ac API.")

            if len(json["items"]) == 0:
                raise IllegalStatementError("No matching open found.")

            random_problem = random.choice(json["items"])

            status.update("Opening in browser...")
            webbrowser.open(
                boj.core.constant.boj_problem_url(random_problem["problemId"])
            )
