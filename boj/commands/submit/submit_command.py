import time

import boj.core.auth
import boj.core.constant
import boj.core.util as util
from boj.commands.submit import websocket
from boj.core.base import Command
from boj.core.config import Config
from boj.data.boj_info import BojInfo
from boj.data.credential import Credential
from boj.core.out import BojConsole
from boj.core import http
from boj.core import constant
from boj.data.solution import Solution
from boj.pages.boj_main_page import BojMainPage
from boj.pages.boj_status_page import BojStatusPage
from boj.pages.boj_submit_page import BojSubmitPage


class SubmitCommand(Command):
    def execute(self, args):
        config = Config.load()

        console = BojConsole()
        with console.status("Loading config...") as status:
            time.sleep(0.23)

            status.update("Looking for problem information...")
            time.sleep(0.21)

            boj_info = BojInfo.find_any(
                problem_dir=config.workspace.problem_dir,
                problem_id=args.problem_id
            )
            console.log("Successfully loaded configuration")

        with console.status("Loading source file...") as status:
            solution = Solution.read(boj_info)

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
            payload = {
                "csrf_key": submit_page.query_csrf_key(),
                "problem_id": solution.id,
                "language": util.convert_language_code(boj_info.language),
                "code_open": args.open,
                "source": solution.source_code,
            }

            status.update("Submitting source code...")
            response = http.post(
                constant.boj_submit_url(solution.id),
                headers=boj.core.constant.default_headers(),
                cookies=credential.session_cookies_of(main_page.online_judge_token()),
                data=payload,
            )
            status_page = BojStatusPage(html=response.text)

            console.log("Submission succeeded")

        console.rule(style="dim white")
        console.print(f"[bold]• [{boj_info.id}] {boj_info.title}")
        message = websocket.subscribe_progress(
            status_page.solution_id(),
            timeout=args.timeout,
        )

        boj_info.checksum = util.file_hash(solution.path)
        boj_info.accepted = (message.status == "Accepted")
        boj_info.save()
