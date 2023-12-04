from pathlib import Path

from boj.core.base import Command
from boj.core.config import Config
from boj.core.error import IllegalStatementError, ResourceNotFoundError
from boj.core import util
import os

from boj.core.out import BojConsole


class InitCommand(Command):
    def execute(self, args):
        console = BojConsole()
        try:
            workspace_root = util.search_file_in_parent_dirs(
                suffix=".boj/config.yaml", cwd=os.path.expanduser(os.getcwd())
            )
            os.makedirs(os.path.join(workspace_root, ".boj"), exist_ok=True)
            os.makedirs(
                os.path.join(workspace_root, ".boj", "templates"), exist_ok=True
            )

            if not util.file_exists(os.path.join(workspace_root, ".boj", "config.yaml")):
                Path(f"{workspace_root}/.boj/config.yaml").touch()

            console.log(f"Reinitialized '{workspace_root}/.boj'")

        except ResourceNotFoundError:  # when not initialized
            cwd = os.path.expanduser(os.getcwd())
            os.makedirs(os.path.join(cwd, ".boj"), exist_ok=True)
            os.makedirs(os.path.join(cwd, ".boj", "templates"), exist_ok=True)

            if not util.file_exists(f"{cwd}/.boj/config.yaml"):
                Path(f"{cwd}/.boj/config.yaml").touch()

            console.log("Successfully initialized BOJ directory")
