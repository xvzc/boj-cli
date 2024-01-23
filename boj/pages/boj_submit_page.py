from typing import cast

from bs4 import BeautifulSoup

from boj.core.error import AuthenticationError
from boj.core.http import HttpRequest, Page
from boj.data.boj_info import BojInfo
from boj.core import constant
from boj.core import http
from boj.core import util
from boj.data.session import Session
from boj.pages.boj_status_page import BojStatusPage


class BojSubmitPageRequest(HttpRequest):
    def __init__(self, boj_info: BojInfo, session: Session):
        super().__init__(
            url=constant.boj_submit_url(boj_info.id),
            headers=constant.default_headers(),
            cookies=session.cookies,
        )


class BojSubmitRequest(HttpRequest):
    def __init__(
        self,
        boj_info: BojInfo,
        session: Session,
        data: dict,
    ):
        super().__init__(
            url=constant.boj_submit_url(boj_info.id),
            headers=constant.default_headers(),
            cookies=session.cookies,
        )
        self.__data = data


class BojSubmitPage(Page):
    # When we send a submit request, it responds the status page if the submission succeeds.
    # Therefore, BojSubmitPage.submit() will return the html content of status page.
    def submit(
        self,
        boj_info: BojInfo,
        session: Session,
        open_: str,
    ) -> BojStatusPage:
        data = {
            "csrf_key": self.__find_csrf_token(),
            "problem_id": boj_info.id,
            "language": util.convert_language_code(boj_info.language),
            "code_open": open_,
            "source": util.read_file(boj_info.source_path).decode("utf-8"),
        }

        response = BojStatusPage.post(
            BojSubmitRequest(
                boj_info=boj_info,
                session=session,
                data=data,
            )
        )

        return response

    def __find_csrf_token(self):
        # Parse the submit page
        soup = BeautifulSoup(self.html, "html.parser")

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
