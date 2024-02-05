from typing import Optional

from bs4 import BeautifulSoup

from boj.core import constant
from boj.core.html import HtmlParser
from boj.core.http import RequestWithParams
from boj.data.testcase import Testcase


class BojProblemPageRequest(RequestWithParams):
    def __init__(self, problem_id: str):
        self.__problem_id = problem_id

    def url(self) -> str:
        return constant.boj_problem_url(self.__problem_id)

    def headers(self) -> Optional[dict]:
        return constant.default_headers()

    def cookies(self) -> Optional[dict]:
        return None

    def params(self) -> Optional[dict]:
        return None


class TitleParser(HtmlParser[str]):
    def find(self, html) -> str:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("span", id="problem_title")
        return title.text


class TestcaseParser(HtmlParser[list[Testcase]]):
    def find(self, html) -> list[Testcase]:
        soup = BeautifulSoup(html, "html.parser")
        sample_data = soup.select("pre.sampledata")

        inputs = []
        outputs = []
        for data in sample_data:
            text = data.text

            if "input" in str(data.get("id", "")):
                inputs.append(text)

            if "output" in str(data.get("id", "")):
                outputs.append(text)

        test_idx = 1
        testcases: list[Testcase] = []
        for data_in, data_out in zip(inputs, outputs):
            testcases.append(
                Testcase(label=str(test_idx), input_=data_in, output=data_out)
            )

            test_idx += 1

        return testcases
