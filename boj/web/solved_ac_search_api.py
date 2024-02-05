from typing import Optional

import requests

from boj.core import constant
from boj.core.http import JsonResponse, HttpRequest, RequestWithParams


def make_solved_ac_search_api_params(
    tags: list[str],
    lang: str,
    tier: str,
    user: str,
    page: int = 1,
    sort: str = "random",
    direction: str = "asc",
):
    tier = f"tier:{tier}" if tier else ""
    solved_by = f"-solved_by:{user}"
    language = f"lang:{lang}" if lang else ""
    tags = f'({" | ".join(["tag:" + tag for tag in tags])})' if tags else ""

    query = " ".join([tier, solved_by, language, tags])

    return {
        "query": query,
        "page": page,
        "sort": sort,
        "direction": direction,
    }


class SolvedAcSearchApiRequest(RequestWithParams):
    def __init__(
        self,
        params: dict,
    ):
        self.__params = params

    def url(self) -> str:
        return constant.solved_ac_search_problem_url()

    def headers(self) -> Optional[dict]:
        return constant.default_headers()

    def cookies(self) -> Optional[dict]:
        return None

    def params(self) -> Optional[dict]:
        return self.__params
