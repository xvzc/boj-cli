from bs4 import BeautifulSoup

from boj.core.error import ParsingHtmlError
from boj.core.html import HtmlParser


class SolutionIdParser(HtmlParser[str]):
    def find(self, html) -> str:
        soup = BeautifulSoup(html, "html.parser")
        soup.select("table", {"id": "status-table"})
        if soup is None:
            raise ParsingHtmlError("Failed to query solution id.")

        soup = soup.select("tr")

        solution_id = str(soup[1]["id"]).split("-")[1]
        return solution_id
