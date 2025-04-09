import dataclasses

from rich.console import Console

from boj.core.command import Command
from boj.core.error import ResourceNotFoundError
from boj.core.fs.file_io import FileIO
from boj.core.fs.repository import ReadOnlyRepository
from boj.core.fs.util import mkdir
import os

from boj.data.config import Config

default_config = """
general:
  selenium_browser: chrome
workspace:
  ongoing_dir: problems
  archive_dir: solved
"""


@dataclasses.dataclass
class InitCommand(Command):
    console: Console
    config_repository: ReadOnlyRepository[Config]
    file_io: FileIO

    def execute(self, args):
        workspace_root = os.path.expanduser(os.getcwd())
        try:
            config = self.config_repository.find()
            self.console.log(f"'{config.metadata.dir}' already exists.")
            return
        except ResourceNotFoundError:  # when not initialized
            mkdir(os.path.join(workspace_root, ".boj", "templates"))
            mkdir(os.path.join(workspace_root, ".boj"))
            self.file_io.write(
                bytes(default_config.lstrip(), "utf-8"),
                os.path.join(workspace_root, ".boj", "config.yaml"),
            )
            self.console.log(f"Successfully initialized '{workspace_root}'.")
