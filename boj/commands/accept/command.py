import dataclasses

from rich.console import Console

from boj.core.command import Command

from boj.core.fs.repository import Repository
from boj.data.config import Config
from boj.data.boj_info import BojInfo
from boj.core.fs.file_object import TextFile

from boj.core.fs.file_search_strategy import StaticSearchStrategy, UpwardSearchStrategy
from boj.web.boj_submit_page import (
    BojSubmitPageRequest,
    BojSubmitPostRequest,
    make_submit_post_body,
)


@dataclasses.dataclass
class AcceptCommand(Command):
    console: Console
    config_repository: Repository[Config]
    boj_info_repository: Repository[BojInfo]
    text_file_repository: Repository[TextFile]

    def execute(self, args):
        config = self.config_repository.find()

        with self.console.status("Loading config..") as status:
            status.update("Looking for problem information..")
            self.boj_info_repository.search_strategy = (
                StaticSearchStrategy() if args.problem_id else UpwardSearchStrategy()
            )
            cwd = config.workspace.search_dir(args.problem_id)
            boj_info = self.boj_info_repository.find(cwd, ".boj-info.json")

            source_code = self.text_file_repository.find(
                cwd=boj_info.metadata.dir,
                query=boj_info.source_path(abs_=False),
            )

        if args.revert:
            boj_info.accepted = False
        else:
            boj_info.accepted = True
            boj_info.checksum = self.text_file_repository.hash(source_code)

        status = "[green]'Accepted'" if boj_info.accepted else "[red]'Not Accepted'"

        self.boj_info_repository.save(boj_info)
        self.console.print(
            f"[white]Successfully updated the problem status to {status}"
        )
