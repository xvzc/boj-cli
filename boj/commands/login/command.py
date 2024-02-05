import dataclasses
import os

from rich.console import Console

from boj.browsers.login_browser import LoginBrowser
from boj.core.error import ParsingConfigError
from boj.core.fs.file_object import FileMetadata
from boj.core.fs.repository import Repository, ReadOnlyRepository
from boj.data.config import Config
from boj.data.credential import Credential
from boj.core import constant
from boj.core.command import Command


@dataclasses.dataclass
class LoginCommand(Command):
    console: Console
    config_repository: ReadOnlyRepository[Config]
    credential_repository: Repository[Credential]

    def execute(self, args):
        config = self.config_repository.find()
        if not config.general.selenium_browser:
            raise ParsingConfigError("Please specify 'config.general.login_browser'")

        with self.console.status("Preparing login browser...") as status:
            browser = LoginBrowser(
                constant.boj_login_url(),
                config.general.selenium_browser,
            )

            browser.open()
            credential_dict = browser.wait_for_login()
            browser.close()

            status.update("Encrypting the credential...")
            credential = Credential(
                metadata=FileMetadata.of(
                    os.path.join(constant.boj_cli_path(), "credential")
                ),
                username=credential_dict["username"],
                token=credential_dict["token"],
            )

            status.update("Writing to file...")
            self.credential_repository.save(credential)

        self.console.print("[green]Login succeeded")
