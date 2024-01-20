import os
import time
from datetime import datetime

import shutil
from boj.core import util
from boj.core.base import Command
from boj.core.config import Config
from boj.core.out import BojConsole
from boj.data.boj_info import BojInfo


class CleanCommand(Command):
    def execute(self, args):
        config = Config.load()
        console = BojConsole()
        with console.status("Preparing...") as status:
            time.sleep(0.46)

            status.update("Looking for accepted problems...")
            time.sleep(0.23)

            tobe_removed = []
            for problem_id in os.listdir(config.workspace.problem_dir):
                time.sleep(0.063)
                problem_root = os.path.join(config.workspace.problem_dir, problem_id)

                skip = False
                log = None

                filename = os.path.join(problem_root, ".boj-info.json")
                if not os.path.isfile(filename) and not log:
                    skip = True
                    log = (
                        f"'{problem_id}' not a directory "
                        + "that has been added via 'boj add'"
                    )

                boj_info = BojInfo.read(dir=problem_root)
                if not boj_info.accepted and not log:
                    skip = True
                    log = (
                        f"'{problem_id}' "
                        + "last submission has not been 'Accepted' yet"
                    )

                checksum = util.file_hash(boj_info.get_source_path())
                if boj_info.checksum != checksum and not log:
                    skip = True
                    log = (
                        f"'{problem_id}' "
                        + "source code has been changed since the last submit"
                    )

                if skip:
                    console.log(f"[red][SKIP][/ red] {log}")
                    continue

                archive_problem_root = os.path.join(
                    config.workspace.archive_dir, problem_id
                )

                os.makedirs(name=archive_problem_root, exist_ok=True)

                dir_, name = os.path.split(boj_info.get_source_path())
                if not args.origin:
                    name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}"

                util.copy_file(
                    from_path=boj_info.get_source_path(),
                    to_path=os.path.join(archive_problem_root, name),
                )

                tobe_removed.append(problem_root)
                log = f"'{problem_id}' successfully archived"
                console.log(f"[green][DONE][/ green] {log}")

            for p in tobe_removed:
                shutil.rmtree(path=p)

            message = (
                f"Archived {len(tobe_removed)} files to "
                + f"'{config.workspace.archive_dir}'"
            )

            console.rule(style="dim white")
            console.print(message)
