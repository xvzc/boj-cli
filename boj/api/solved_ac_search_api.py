import requests

from boj.core import constant
from boj.core.base import Api


class SolvedAcSearchApiParam:
    tags: list[str]
    lang: str
    tier: str
    user: str

    def __init__(self, tags, lang, tier, user):
        self.tags = tags
        self.lang = lang
        self.tier = tier
        self.user = user

    def to_query_string(self):
        tier_query = f"tier:{self.tier}"
        solved_by_query = f"-solved_by:{self.user}"
        language_query = f"lang:{self.lang}"
        tags_query = f'({" | ".join(["tag:" + tag for tag in self.tags ])})'

        return " ".join(
            [
                tier_query,
                solved_by_query,
                language_query,
                tags_query,
            ]
        )


class SolvedAcSearchApi(Api):
    url: str
    param: SolvedAcSearchApiParam

    def __init__(self, url: str, param: SolvedAcSearchApiParam):
        self.url = url
        self.param = param

    def request(self):
        params = {
            "query": self.param.to_query_string(),
            "page": 1,
            "sort": "random",
            "direction": "asc",
        }

        response = requests.get(headers=constant.default_headers(), url=self.url, params=params)
        return response
