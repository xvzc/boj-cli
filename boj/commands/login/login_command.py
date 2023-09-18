import time

from boj.browsers.login_browser import LoginBrowser
from boj.core import auth
from boj.core import constant
from boj.core import util
from boj.core.base import Command
from boj.core.config import Config
from boj.core.out import BojConsole


class LoginCommand(Command):
    def execute(self, args, config: Config):

        console = BojConsole()
        with console.status("Preparing login browser...") as status:
            browser = LoginBrowser(constant.boj_login_url())
            browser.open()
            credential = browser.wait_for_login()
            browser.close()

            status.update("Creating an encryption key...")
            key = auth.create_key()
            time.sleep(0.3)

            status.update("Encrypting the credential...")
            time.sleep(0.3)
            encrypted = auth.encrypt(key, credential.to_json())

            status.update("Writing to file...")
            time.sleep(0.3)
            util.write_file(constant.key_file_path(), key, "wb")
            util.write_file(constant.credential_file_path(), encrypted, "wb")

        console.print("[green]Login succeeded")
