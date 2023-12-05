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
            suffix = os.path.join(".boj", "config.yaml")
            workspace_root = util.search_file_in_parent_dirs(
                suffix=suffix, cwd=os.path.expanduser(os.getcwd())
            ).replace(os.path.join("", suffix), "")
            message = f"Reinitialized '{os.path.join(workspace_root, '.boj')}'"

        except ResourceNotFoundError:  # when not initialized
            workspace_root = os.path.expanduser(os.getcwd())
            message = (
                f"Successfully initialized '{os.path.join(workspace_root, '.boj')}'"
            )

        os.makedirs(os.path.join(workspace_root, ".boj"), exist_ok=True)
        os.makedirs(os.path.join(workspace_root, ".boj", "templates"), exist_ok=True)

        if not util.file_exists(os.path.join(workspace_root, ".boj", "config.yaml")):
            Path(os.path.join(workspace_root, ".boj", "config.yaml")).touch()

        console.log(message)
