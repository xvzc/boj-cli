from requests.cookies import RequestsCookieJar

from boj.core.base import Page


class BojMainPage(Page):
    html: str
    cookies: RequestsCookieJar

    def __init__(self, html, cookies):
        self.html = html
        self.cookies = cookies

    def online_judge_token(self):
        return self.cookies.get_dict()["OnlineJudge"]
