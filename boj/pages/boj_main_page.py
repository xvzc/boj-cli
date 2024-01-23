from requests.cookies import RequestsCookieJar

from boj.core import constant
from boj.core import http
from boj.core.http import HttpRequest, Page
from boj.data.credential import Credential
from boj.data.session import Session


class BojMainPageRequest(HttpRequest):
    def __init__(self):
        super().__init__(
            url=constant.boj_main_url(),
            headers=constant.default_headers(),
            cookies=None,
        )

    @property
    def url(self) -> str:
        return constant.boj_main_url()

    @property
    def headers(self):
        return constant.default_headers()

    @property
    def cookies(self):
        return None


class BojMainPage(Page):
    def make_session(self, credential: Credential) -> Session:
        return Session(
            credential=credential,
            online_judge=self.cookies["OnlineJudge"],
        )
