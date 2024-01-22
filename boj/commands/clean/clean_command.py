import os
from datetime import datetime

import shutil
from boj.core import util
from boj.core.base import Command
from boj.data.config import Config
from boj.core.out import BojConsole
from boj.data.boj_info import BojInfo


class Items:
    def __init__(self, skip, message, dir):
        self.skip = skip
        self.message = message
        self.dir = dir


class CleanCommand(Command):
    def execute(self, args):
        config = Config.load()
        console = BojConsole()

        with console.status("Preparing...") as status:
            status.update("Looking for accepted problems...")

            items = []
            for problem_id in os.listdir(config.__workspace.__ongoing_dir):
                problem_root = os.path.join(config.__workspace.__ongoing_dir, problem_id)

                filename = os.path.join(problem_root, ".boj-info.json")
                if not os.path.isfile(filename):
                    message = (
                        f"'{problem_id}' not a directory "
                        + "that has been added via 'boj add'"
                    )
                    items.append(Items(skip=True, message=message, dir=problem_root))
                    continue

                boj_info = BojInfo.read(dir_=problem_root)
                if not boj_info.__accepted:
                    message = (
                        f"'{problem_id}' "
                        + "last submission has not been 'Accepted' yet"
                    )
                    items.append(Items(skip=True, message=message, dir=problem_root))
                    continue

                checksum = util.file_hash(boj_info.source_path())
                if boj_info.__checksum != checksum:
                    message = (
                        f"'{problem_id}' "
                        + "source code has been changed since the last submit"
                    )
                    items.append(Items(skip=True, message=message, dir=problem_root))
                    continue

                archive_problem_root = os.path.join(
                    config.__workspace.__archive_dir, problem_id
                )

                os.makedirs(name=archive_problem_root, exist_ok=True)

                dir_, name = os.path.split(boj_info.source_path())
                if not args.origin:
                    name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}"

                util.copy_file(
                    from_path=boj_info.source_path(),
                    to_path=os.path.join(archive_problem_root, name),
                )

                message = f"'{problem_id}' archived"
                items.append(Items(skip=False, message=message, dir=problem_root))

            skip_cnt = sum(i.skip for i in items)
            done_cnt = len(items) - skip_cnt

            if skip_cnt > 0 or done_cnt > 0:
                console.rule(style="dim white")

            for item in items:
                if item.skip:
                    console.log(f"[yellow][SKIP][/ yellow] {item.message}")
                else:
                    console.log(f"[green][DONE][/ green] {item.message}")
                    shutil.rmtree(path=item.dir)

            console.rule(style="dim white")
            console.log(
                f"Archived {done_cnt} files to '{config.__workspace.__archive_dir}'"
            )
