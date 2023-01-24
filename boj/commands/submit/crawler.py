import requests
from bs4 import BeautifulSoup
import boj.core.util as util


def query_online_judge_token(url):
    response = requests.get(url, headers=util.headers())
    return response.cookies.get_dict()["OnlineJudge"]


def query_csrf_key(url, cookies):
    response = requests.get(url, headers=util.headers(), cookies=cookies)

    # Parse the submit page
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    input_tags = soup.select("input")
    check_login_status(input_tags)

    # Get the csrf_key
    csrf_key = ""
    for i in input_tags:
        if i["name"] == "csrf_key":
            csrf_key = i["value"]

    if not csrf_key:
        raise Exception("Could not query csrf_key")

    return csrf_key


def send_source_code(url, cookies, payload):
    util.print_white("\rSubmitting source code. ")

    response = requests.post(url, headers=util.headers(), cookies=cookies, data=payload)

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    util.print_white("\rSubmitting source code.. ")

    soup.select("table", {"id": "status-table"})
    if soup is None:
        raise Exception("Failed to query solution id.")

    util.print_white("\rSubmitting source code... ")

    soup = soup.select("tr")

    solution_id = str(soup[1]["id"]).split("-")[1]
    return solution_id


def check_login_status(input_tags):
    for i in input_tags:
        if i["name"] == "login_user_id":
            raise Exception("Login Required.")
