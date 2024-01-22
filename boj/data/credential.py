import json
import os

from boj.core.error import AuthenticationError
from boj.core import util
from boj.core import crypto


class Credential:
    def __init__(self, username, token):
        self.__username = username
        self.__token = token

    @property
    def username(self):
        return self.__username

    @property
    def token(self):
        return self.__token

    def __repr__(self):
        return "Credential {" + str(self.__username) + ", " + self.__token + "}"

    def __eq__(self, other):
        return self.__username == other.__username and self.__token == other.__token

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def make_session_cookies(self, online_judge_token):
        return {"bojautologin": self.__token, "OnlineJudge": online_judge_token}


class CredentialIO:
    def __init__(self, dir_: str):
        self.__dir = dir_

    @property
    def dir(self):
        return self.__dir

    def __key_path(self) -> str:
        return os.path.join(self.__dir, "key")

    def __credential_path(self) -> str:
        return os.path.join(self.__dir, "credential")

    def read(self) -> Credential:
        try:
            key = util.read_file(self.__key_path())
            credential = util.read_file(self.__credential_path())
            decrypted = json.loads(crypto.decrypt(key, credential))
            return Credential(username=decrypted["username"], token=decrypted["token"])
        except Exception:
            raise AuthenticationError("Failed to read the credential")

    def save(self, credential: Credential) -> None:
        key = crypto.create_key()
        util.write_file(self.__key_path(), key)
        util.write_file(
            self.__credential_path(), crypto.encrypt(key, credential.to_json())
        )
