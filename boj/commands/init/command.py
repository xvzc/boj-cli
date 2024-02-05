import dataclasses
from pathlib import Path

from rich.console import Console

from boj.core.command import Command
from boj.core.error import ResourceNotFoundError
from boj.core.fs.repository import ReadOnlyRepository
from boj.core.fs.util import mkdir
import os

from boj.data.config import Config


@dataclasses.dataclass
class InitCommand(Command):
    console: Console
    config_repository: ReadOnlyRepository[Config]

    def execute(self, args):
        workspace_root = os.path.expanduser(os.getcwd())
        try:
            config = self.config_repository.find()
            self.console.log(f"'{config.metadata.dir}' already exists. Reinitializing..")
        except ResourceNotFoundError:  # when not initialized
            mkdir(os.path.join(workspace_root, ".boj"))
            Path(os.path.join(workspace_root, ".boj", "config.yaml")).touch()

        mkdir(os.path.join(workspace_root, ".boj", "templates"))
        self.console.log(f"Successfully initialized '{workspace_root}'.")
