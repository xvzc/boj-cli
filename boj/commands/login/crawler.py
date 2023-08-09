import requests
from bs4 import BeautifulSoup
from boj.core import util


def check_login_status(url, username, bojautologin, online_judge):
    cookies = {
        "bojautologin": bojautologin,
        "OnlineJudge": online_judge,
    }

    response = requests.get(
        url,
        headers=util.headers(),
        cookies=cookies
    )

    # Parse the submit page
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    username_tag = soup.select("a.username")
    if username != username_tag[0].text:
        return False

    response_cookies = response.cookies.get_dict()
    if "bojautologin" not in response_cookies:
        return False

    return True
