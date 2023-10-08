import boj.core.auth
import boj.core.constant
import boj.core.util as util
from boj.commands.submit import websocket
from boj.core.base import Command
from boj.core.config import Config
from boj.core.data import Credential
from boj.core.out import BojConsole
from boj.core import http
from boj.core import constant
from boj.pages.boj_main_page import BojMainPage
from boj.pages.boj_status_page import BojStatusPage
from boj.pages.boj_submit_page import BojSubmitPage


class SubmitCommand(Command):
    def execute(self, args, config: Config):
        console = BojConsole()

        with console.status("Loading source file...") as status:
            solution = util.read_solution(args.file)

            status.update("Authenticating...")
            credential: Credential = boj.core.auth.read_credential()

            response = http.get(
                url=constant.boj_main_url(), headers=constant.default_headers()
            )
            main_page = BojMainPage(html=response.text, cookies=response.cookies)

            response = http.get(
                url=constant.boj_submit_url(solution.id),
                headers=constant.default_headers(),
                cookies=credential.session_cookies_of(main_page.online_judge_token()),
            )

            submit_page = BojSubmitPage(html=response.text)

            # Set payload for the submit request
            language = (
                args.lang or config.filetype_config_of(solution.filetype).default_language
            )
            payload = {
                "csrf_key": submit_page.query_csrf_key(),
                "problem_id": solution.id,
                "language": util.convert_language_code(language),
                "code_open": args.open or config.command.submit.open,
                "source": solution.source,
            }

            status.update("Submitting source code...")
            response = http.post(
                constant.boj_submit_url(solution.id),
                headers=boj.core.constant.default_headers(),
                cookies=credential.session_cookies_of(main_page.online_judge_token()),
                data=payload,
            )
            status_page = BojStatusPage(html=response.text)

            console.log("Submission succeeded.")

        websocket.subscribe_progress(status_page.solution_id())
