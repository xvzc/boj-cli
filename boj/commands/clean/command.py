import dataclasses
import os
from datetime import datetime

import shutil

from rich.console import Console

from boj.core.command import Command
from boj.core.error import ResourceNotFoundError
from boj.core.fs.file_object import TextFile
from boj.core.fs.repository import ReadOnlyRepository, Repository
from boj.data.config import Config
from boj.data.boj_info import BojInfo


class Items:
    def __init__(self, skip, message, dir_):
        self.skip = skip
        self.message = message
        self.dir = dir_


@dataclasses.dataclass
class CleanCommand(Command):
    console: Console
    config_repository: ReadOnlyRepository[Config]
    boj_info_repository: Repository[BojInfo]
    text_file_repository: Repository[TextFile]

    def execute(self, args):
        config = self.config_repository.find()

        with self.console.status("Preparing...") as status:
            status.update("Looking for accepted problems...")

            items = []
            ongoing_dir = config.workspace.ongoing_dir(abs_=True)
            for problem_id in os.listdir(ongoing_dir):
                problem_root = config.workspace.problem_dir(problem_id)
                cwd, query, search_strategy = BojInfo.query_factory(
                    config.workspace.ongoing_dir(abs_=True),
                    problem_id,
                )

                self.boj_info_repository.strategy = search_strategy

                try:
                    boj_info = self.boj_info_repository.find(cwd, query)
                except ResourceNotFoundError as e:
                    message = (
                        f"'{problem_id}' is not a directory "
                        + "that has been added via 'boj add'"
                    )
                    items.append(Items(skip=True, message=message, dir_=problem_root))
                    continue

                if not boj_info.accepted:
                    message = (
                        f"'{problem_id}' "
                        + "last submission has not been 'Accepted' yet"
                    )
                    items.append(Items(skip=True, message=message, dir_=problem_root))
                    continue

                source_code = self.text_file_repository.find(
                    cwd=boj_info.metadata.dir,
                    query=boj_info.source_path(abs_=False),
                )
                checksum = self.text_file_repository.hash(source_code)
                if boj_info.checksum != checksum:
                    message = (
                        f"'{problem_id}' "
                        + "source code has been changed since the last submit"
                    )
                    items.append(Items(skip=True, message=message, dir_=problem_root))
                    continue

                if not args.origin:
                    time_format = datetime.now().strftime("%Y%m%d_%H%M%S")
                    archive_name = f"{time_format}_{source_code.metadata.name}"

                archive_dir = os.path.join(
                    config.workspace.archive_dir(problem_id, abs_=True)
                )
                self.text_file_repository.copy(
                    obj=source_code,
                    dest=os.path.join(archive_dir, archive_name),
                )

                message = f"'{problem_id}' archived"
                items.append(Items(skip=False, message=message, dir_=problem_root))

            skip_cnt = sum(i.skip for i in items)
            done_cnt = len(items) - skip_cnt

            if skip_cnt > 0 or done_cnt > 0:
                self.console.rule(style="dim white")

            for item in items:
                if item.skip:
                    self.console.log(f"[yellow][SKIP][/ yellow] {item.message}")
                else:
                    self.console.log(f"[green][DONE][/ green] {item.message}")
                    shutil.rmtree(path=item.dir)

            self.console.rule(style="dim white")
            self.console.log(f"Archived {done_cnt} files")
