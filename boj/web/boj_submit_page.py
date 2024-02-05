from typing import Optional

from bs4 import BeautifulSoup

from boj.core import constant
from boj.core.error import AuthenticationError
from boj.core.fs.file_object import TextFile
from boj.core.html import HtmlParser
from boj.core.http import RequestWithParams, RequestWithBody
from boj.data.boj_info import BojInfo
from boj.data.session import Session


def make_submit_post_body(
    boj_info: BojInfo, csrf_key: str, source_code: TextFile, open_: str
):
    return {
        "csrf_key": csrf_key,
        "problem_id": boj_info.id,
        "language": boj_info.language,
        "code_open": open_,
        "source": source_code.content,
    }


class BojSubmitPageRequest(RequestWithParams):
    def __init__(self, problem_id: int, cookies: dict):
        self.__problem_id = problem_id
        self.__cookies = cookies

    def url(self) -> str:
        return constant.boj_submit_url(self.__problem_id)

    def headers(self) -> Optional[dict]:
        return constant.default_headers()

    def cookies(self) -> Optional[dict]:
        return self.__cookies

    def params(self) -> Optional[dict]:
        return None


class BojSubmitPostRequest(RequestWithBody):
    def __init__(
        self,
        problem_id: int,
        cookies: dict,
        data: dict,
    ):
        self.__problem_id = problem_id
        self.__cookies = cookies
        self.__data = data

    def url(self) -> str:
        return constant.boj_submit_url(self.__problem_id)

    def headers(self) -> Optional[dict]:
        return constant.default_headers()

    def cookies(self) -> Optional[dict]:
        return self.__cookies

    def data(self) -> Optional[dict]:
        return self.__data


class CsrfKeyParser(HtmlParser):
    def find(self, html) -> str:
        # Parse the submit page
        soup = BeautifulSoup(html, "html.parser")

        # Check login status
        input_tags = soup.select("input")
        for tag in input_tags:
            if tag["name"] == "login_user_id":
                raise AuthenticationError(
                    "Authentication failed. Did you run 'boj login'?"
                )

        # Get the csrf_key
        for tag in input_tags:
            if tag["name"] == "csrf_key":
                return tag["value"]

        raise AuthenticationError("Failed to query csrf token.")
