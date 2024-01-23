from bs4 import BeautifulSoup

from boj.core.http import HttpRequest, Page
from boj.data.testcase import Testcase
from boj.core import util
from boj.core import http
from boj.core import constant


class BojProblemPageRequest(HttpRequest):
    def __init__(self, problem_id: str):
        super().__init__(
            url=constant.boj_submit_url(problem_id),
            headers=constant.default_headers(),
        )


class BojProblemPage(Page):

    def find_testcases(self):
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
            testcases.append(Testcase(label=test_idx, input_=data_in, output=data_out))

            test_idx += 1

        return testcases

    def find_title(self):
        soup = BeautifulSoup(self.html, "html.parser")
        title = soup.find("span", id="problem_title")
        return title.text
