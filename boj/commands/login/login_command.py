import os
import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from boj.browsers.login_browser import LoginBrowser
from boj.core import auth
from boj.core import property
from boj.core import util
import json

from boj.core.base import Command
from boj.core.out import BojConsole
import chromedriver_autoinstaller
from selenium import webdriver


class LoginCommand(Command):
    def execute(self, args):
        browser = LoginBrowser(property.boj_login_url())
        browser.open()
        credential = browser.wait_for_login()
        browser.close()

        console = BojConsole()
        with console.status("Creating an encryption key...") as status:
            key = auth.create_key()
            time.sleep(0.3)

            status.update("Encrypting the credential...")
            time.sleep(0.3)
            encrypted = auth.encrypt(key, credential.to_json())

            status.update("Writing to file...")
            time.sleep(0.3)
            util.write_file(property.key_file_path(), key, "wb")
            util.write_file(property.credential_file_path(), encrypted, "wb")

        console.print("[green]Login succeeded")
