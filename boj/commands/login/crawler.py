import requests
from boj.core import util


def query_autologin_token(url, bojautologin, online_judge):
    cookies = {
        "bojautologin": bojautologin,
        "OnlineJudge": online_judge,
    }

    response = requests.get(
        url,
        headers=util.headers(),
        cookies=cookies
    )
    response_cookies = response.cookies.get_dict()

    if "bojautologin" not in response_cookies:
        return ""

    return response_cookies["bojautologin"]
