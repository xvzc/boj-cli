import dataclasses
import random
import webbrowser

from rich.console import Console

import boj.core.crypto
import boj.core.constant
from boj.core import constant
from boj.core.command import Command

from boj.core import http
from boj.core.error import IllegalStatementError
from boj.web.solved_ac_search_api import (
    SolvedAcSearchApiRequest,
    make_solved_ac_search_api_params,
)
from boj.core.fs.repository import Repository
from boj.core.http import JsonResponse
from boj.data.credential import Credential


@dataclasses.dataclass
class RandomCommand(Command):
    console: Console
    credential_repository: Repository[Credential]

    def execute(self, args):
        with self.console.status("Reading credential...") as status:
            credential = self.credential_repository.find(cwd=constant.boj_cli_path())

            status.update("Calling solved.ac API...")
            response = JsonResponse(
                http.get(
                    SolvedAcSearchApiRequest(
                        params=make_solved_ac_search_api_params(
                            tags=args.tags,
                            lang="ko",
                            tier=args.tier,
                            user=credential.username,
                        )
                    )
                )
            )

            json = response.json
            if not json or ("items" not in json):
                raise IllegalStatementError("Error while calling solve.ac API.")

            if len(json["items"]) == 0:
                raise IllegalStatementError("No matching problem found.")

            items = json["items"]
            selected_tag = None
            if args.tags:
                selected_tag = random.choice(args.tags)

            for item in items:
                for tag in item["tags"]:
                    if not selected_tag or (tag["key"] == selected_tag):
                        selected_item = item
                        break

            status.update("Opening in browser...")
            webbrowser.open(
                boj.core.constant.boj_problem_url(selected_item["problemId"])
            )
