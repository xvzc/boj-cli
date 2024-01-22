from boj.browsers.login_browser import LoginBrowser
from boj.data.credential import Credential, CredentialIO
from boj.core import constant
from boj.core.base import Command
from boj.core.out import BojConsole


class LoginCommand(Command):
    def execute(self, args):
        console = BojConsole()
        with console.status("Preparing login browser...") as status:
            browser = LoginBrowser(constant.boj_login_url())
            browser.open()
            credential_dict = browser.wait_for_login()
            browser.close()

            status.update("Encrypting the credential...")
            credential_io = CredentialIO(dir_=constant.boj_cli_path())
            credential = Credential(
                username=credential_dict["username"], token=credential_dict["token"]
            )

            status.update("Writing to file...")
            credential_io.save(credential)

        console.print("[green]Login succeeded")
