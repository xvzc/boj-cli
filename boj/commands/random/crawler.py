import requests
from boj.core import util


def create_problem_query(user, tier, level):
    # default == 'all'
    query = "lang:ko tier:" + tier[:1] + "1" + ".." + tier[:1] + "5"

    if level == "easy":
        query = "lang:ko tier:" + tier[:1] + "5"

    if level == "normal":
        query = "lang:ko tier:" + tier[:1] + "3" + ".." + tier[:1] + "4"

    if level == "hard":
        query = "lang:ko tier:" + tier[:1] + "1" + ".." + tier[:1] + "2"

    query += " -solved_by:" + user

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
