import time

from boj.core import http
from boj.core import property
from boj.core import util
from boj.core.base import Command
from boj.core.out import BojConsole
from boj.pages.problem_page import BojProblemPage


class InitCommand(Command):
    def execute(self, args):
        console = BojConsole()
        with console.status("Creating testcases...") as status:
            time.sleep(0.5)
            response = http.get(
                url=property.boj_problem_url(args.problem_id),
                headers=property.headers(),
            )

            problem_page = BojProblemPage(html=response.text)

            testcases = problem_page.extract_testcases()
            yaml_testcases = util.testcases_to_yaml(testcases)

            util.write_file(property.testcase_file_path(), yaml_testcases, "w")
            console.print("Testcases have been created.")
