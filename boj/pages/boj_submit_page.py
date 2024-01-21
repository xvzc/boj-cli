from bs4 import BeautifulSoup

from boj.core.base import Page
from boj.core.error import AuthenticationError


class BojSubmitPage(Page):
    html: str
    # online_judge: str
    # credential: Credential

    def __init__(self, html):
        self.html = html
        # self.online_judge = online_judge
        # self.credential = credential

    def query_csrf_key(self):
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
