import time

from boj.core import http
from boj.core import constant
from boj.core import util
from boj.core.base import Command
from boj.core.config import Config
from boj.core.out import BojConsole
from boj.pages.problem_page import BojProblemPage


class InitCommand(Command):
    def execute(self, args, config: Config):
        console = BojConsole()
        with console.status("Creating testcases...") as status:
            time.sleep(0.5)
            response = http.get(
                url=constant.boj_problem_url(args.problem_id),
                headers=constant.default_headers(),
            )

            problem_page = BojProblemPage(html=response.text)

            testcases = problem_page.extract_testcases()
            yaml_testcases = util.testcases_to_yaml_content(testcases)

            util.write_file(constant.testcase_file_path(), yaml_testcases, "w")
            console.print("Testcases have been created.")
