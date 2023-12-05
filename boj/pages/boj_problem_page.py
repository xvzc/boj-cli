from bs4 import BeautifulSoup

from boj.core.base import Page
from boj.data.testcase import Testcase
from boj.core import util


class BojProblemPage(Page):
    def __init__(self, html):
        self.html = html

    def extract_testcases(self):
        soup = BeautifulSoup(self.html, "html.parser")
        sample_data = soup.select("pre.sampledata")

        inputs = []
        outputs = []
        for data in sample_data:
            text = util.normalize(data.text)

            if "input" in str(data.get("id", "")):
                inputs.append(text)

            if "output" in str(data.get("id", "")):
                outputs.append(text)

        test_idx = 1
        testcases: list[Testcase] = []
        for data_in, data_out in zip(inputs, outputs):
            testcases.append(
                Testcase(
                    label=test_idx,
                    data_in=data_in,
                    data_out=data_out
                )
            )

            test_idx += 1

        return testcases

    def extract_title(self):
        soup = BeautifulSoup(self.html, "html.parser")
        title = soup.find("span", id = "problem_title")
        return title.text
