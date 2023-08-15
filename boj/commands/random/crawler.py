import requests
from boj.core import util


def create_problem_query(user, tier, tags):
    tier_query = f'tier:{tier}'
    solved_by_query = f'-solved_by:{user}'
    language_query = "lang:ko"
    tags_query = f'({" | ".join(["tag:" + tag for tag in tags ])})'

    query = " ".join([
        tier_query, 
        solved_by_query, 
        language_query,
        tags_query, 
    ])

    params = {
        'query': query,
        'page': 1,
        'sort': 'random',
        'direction': 'asc'
    }

    return params


def query_random_problems(params):
    response = requests.get(headers=util.headers(), url=util.solvedac_search_problem_url(), params=params)
    if response.ok:
        return response.json()

    return None
