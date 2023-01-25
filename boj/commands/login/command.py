import os
import boj.core.auth as auth
import boj.core.util as util
import json


def run(args):
    credential = {
        "user": args.user,
        "token": args.token,
    }

    key = auth.create_key()
    encrypted = auth.encrypt(key, json.dumps(credential))

    try:
        os.makedirs(util.temp_dir(), exist_ok=True)
    except OSError as e:
        raise e

    util.write_file(util.key_file_path(), key, "wb")
    util.write_file(util.credential_file_path(), encrypted, "wb")

    print("Login Success!")

    return
