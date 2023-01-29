import os
import time

import boj.core.auth as auth
import boj.core.util as util
from boj.commands.login import crawler as login_crawler
import json

from boj.core.console import BojConsole
from boj.commands.submit import crawler as submit_crawler


def execute(args):
    credential = {
        "user": args.user,
        "token": args.token,
    }
    console = BojConsole()

    with console.status("Creating key...") as status:
        key = auth.create_key()
        time.sleep(0.3)

        status.update("Encrypting the credential...")
        time.sleep(0.3)
        encrypted = auth.encrypt(key, json.dumps(credential))

        try:
            os.makedirs(util.temp_dir(), exist_ok=True)
        except OSError as e:
            raise e

        status.update("Writing to file...")
        time.sleep(0.3)
        util.write_file(util.key_file_path(), key, "wb")
        util.write_file(util.credential_file_path(), encrypted, "wb")

        status.update("Checking session...")
        online_judge = submit_crawler.query_online_judge_token(util.home_url())
        token = login_crawler.query_autologin_token(
            url=util.home_url(),
            bojautologin=credential['token'],
            online_judge=online_judge
        )

    if token == credential['token']:
        console.print("[green]Login success")
        return

    console.print("[red]Login failed")
