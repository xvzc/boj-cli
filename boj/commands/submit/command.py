import dataclasses

from rich.console import Console

from boj.core.command import Command
from boj.core import http
from boj.core.fs.file_object import TextFile
from boj.core.fs.repository import Repository
from boj.core.html import HtmlParser
from boj.core.http import HtmlResponse
from boj.data.config import Config
from boj.data.boj_info import BojInfo
from boj.core import constant
from boj.data.credential import Credential
from boj.data.session import Session
from boj.web.boj_main_page import BojMainPageRequest
from boj.web.boj_submit_page import (
    BojSubmitPageRequest,
    BojSubmitPostRequest,
    make_submit_post_body,
)
from boj.commands.submit import websocket


@dataclasses.dataclass
class SubmitCommand(Command):
    console: Console
    config_repository: Repository[Config]
    boj_info_repository: Repository[BojInfo]
    credential_repository: Repository[Credential]
    text_file_repository: Repository[TextFile]
    csrf_key_parser: HtmlParser[str]
    solution_id_parser: HtmlParser[str]

    def execute(self, args):
        config = self.config_repository.find()

        with self.console.status("Loading config..") as status:
            status.update("Looking for problem information..")
            cwd, query, search_strategy = BojInfo.query_factory(
                config.workspace.ongoing_dir(abs_=True),
                args.problem_id,
            )
            self.boj_info_repository.search_strategy = search_strategy
            boj_info = self.boj_info_repository.find(cwd, query)

            status.update("Authenticating..")
            credential = self.credential_repository.find(cwd=constant.boj_cli_path())
            main_page = HtmlResponse(http.get(BojMainPageRequest()))
            session = Session(credential, main_page.cookies)

            status.update("Reading source code..")
            submit_page = HtmlResponse(
                http.get(BojSubmitPageRequest(boj_info.id, session.session_cookies))
            )
            csrf_key = self.csrf_key_parser.find(submit_page.html)

            source_code = self.text_file_repository.find(
                cwd=boj_info.metadata.dir,
                query=boj_info.source_path(abs_=False),
            )

            status.update("Submitting source code..")
            session_cookies = session.session_cookies
            data = make_submit_post_body(boj_info, csrf_key, source_code, args.open)
            status_page = HtmlResponse(
                http.post(BojSubmitPostRequest(boj_info.id, session_cookies, data))
            )
            solution_id = self.solution_id_parser.find(status_page.html)

        self.console.rule(style="dim white")
        self.console.print(f"• [{boj_info.id}] {boj_info.title}")

        message = websocket.subscribe_progress(solution_id, args.timeout)
        boj_info.accepted = message.status == "Accepted"
        boj_info.checksum = self.text_file_repository.hash(source_code)
        self.boj_info_repository.save(boj_info)
