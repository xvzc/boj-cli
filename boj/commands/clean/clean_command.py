import os
import time
from datetime import datetime

import shutil
from boj.core import util
from boj.core.base import Command
from boj.core.config import Config
from boj.core.error import ParsingConfigError
from boj.core.out import BojConsole
from boj.data.boj_info import BojInfo


class CleanCommand(Command):
    def execute(self, args):
        config = Config.load()
        console = BojConsole()
        with console.status("Preparing...") as status:
            time.sleep(0.46)
            if config.workspace.problem_dir == config.workspace.archive_dir:
                raise ParsingConfigError("'problem_dir' and 'archive_dir' can not be the same")

            status.update("Looking for accepted problems...")
            time.sleep(0.46)

            tobe_removed = []
            for problem_id in os.listdir(config.workspace.problem_dir):
                time.sleep(0.1)
                problem_root = os.path.join(config.workspace.problem_dir, problem_id)
                if not os.path.isfile(os.path.join(problem_root, ".boj-info.json")):
                    console.log(f"[red][SKIP][/ red] '{problem_id}' not a directory that has been added via 'boj add'")
                    continue

                boj_info = BojInfo.read(problem_root=problem_root)
                if not boj_info.accepted:
                    console.log(f"[red][SKIP][/ red] '{problem_id}' last submission has not been 'Accepted' yet")
                    continue

                checksum = util.file_hash(boj_info.get_source_path())
                if boj_info.checksum != checksum:
                    console.log(f"[red][SKIP][/ red] '{problem_id}' source code has been changed since the last submit")
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
                console.log(f"[green][DONE][/ green] '{problem_id}' successfully archived")

            for p in tobe_removed:
                shutil.rmtree(path=p)

            console.rule(style="dim white")
            console.print(f"Archived {len(tobe_removed)} files to '{config.workspace.archive_dir}'")

