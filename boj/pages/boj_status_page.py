from bs4 import BeautifulSoup

from boj.core.base import Page
from boj.core.error import ParsingHtmlError


class BojStatusPage(Page):
    html: str

    def __init__(self, html):
        self.html = html

    def solution_id(self):
        soup = BeautifulSoup(self.html, "html.parser")
        soup.select("table", {"id": "status-table"})
        if soup is None:
            raise ParsingHtmlError("Failed to query solution id.")

        soup = soup.select("tr")

        solution_id = str(soup[1]["id"]).split("-")[1]
        return solution_id
