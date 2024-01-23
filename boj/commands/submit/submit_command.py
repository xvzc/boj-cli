import boj.core.util as util
from boj.commands.submit import websocket
from boj.core.base import Command
from boj.data.config import Config
from boj.data.boj_info import BojInfo
from boj.core.out import BojConsole
from boj.core import constant
from boj.pages.boj_main_page import BojMainPage, BojMainPageRequest
from boj.pages.boj_submit_page import BojSubmitPage, BojSubmitPageRequest
from boj.data.credential import CredentialIO


class SubmitCommand(Command):
    def execute(self, args):
        config = Config.load()

        console = BojConsole()
        with console.status("Loading config..") as status:
            status.update("Looking for problem information..")
            boj_info = BojInfo.find_any(
                ongoing_dir=config.workspace.ongoing_dir,
                problem_id=args.problem_id,
            )

            status.update("Authenticating..")
            credential_io = CredentialIO(dir_=constant.boj_cli_path())
            credential = credential_io.read()

            status.update("Loading source file..")

            status.update("Submitting source code..")
            main_page = BojMainPage.get(BojMainPageRequest())
            session = main_page.make_session(credential)
            submit_page = BojSubmitPage.get(
                BojSubmitPageRequest(
                    boj_info=boj_info,
                    session=session,
                )
            )

            status_page = submit_page.submit(
                boj_info=boj_info,
                session=session,
                open_=args.open,
            )

        console.rule(style="dim white")
        console.print(f"[bold]• [{boj_info.id}] {boj_info.title}")
        message = websocket.subscribe_progress(
            status_page.find_solution_id(),
            timeout=args.timeout,
        )

        boj_info.checksum = util.file_hash(boj_info.source_path)
        boj_info.accepted = message.status == "Accepted"
        boj_info.save()
