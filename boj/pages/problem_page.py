from bs4 import BeautifulSoup

from boj.core.base import Page
from boj.core.data import Testcase
from boj.core import constant


class BojProblemPage(Page):
    def __init__(self, html):
        self.html = html

    def extract_testcases(self):
        soup = BeautifulSoup(self.html, "html.parser")
        sample_data = soup.select("pre.sampledata")

        inputs = []
        outputs = []
        for data in sample_data:
            text = data.text

            if "input" in str(data.get("id", "")):
                text = text.rstrip()
                inputs.append(text.rstrip())

            if "output" in str(data.get("id", "")):
                text = text.rstrip()
                outputs.append(text.rstrip())

        test_idx = 1
        testcases: list[Testcase] = []
        for data_in, data_out in zip(inputs, outputs):
            testcases.append(
                Testcase(
                    data_in=constant.salt() + data_in + "\n",
                    data_out=constant.salt() + data_out + "\n",
                )
            )

            test_idx += 1

        return testcases
