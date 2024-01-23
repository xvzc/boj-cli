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
        return "Credential { " + str(self.__username) + ", " + self.__token + " }"

    def __eq__(self, other):
        return self.__username == other.__username and self.__token == other.__token

    def to_json(self):
        return json.dumps(
            {
                "username": self.__username,
                "token": self.__token,
            },
            indent=4,
        )

    @classmethod
    def of_json(cls, json_str: str):
        obj = json.loads(json_str)
        return Credential(username=obj["username"], token=obj["token"])

    def make_session_cookies(self, cookies: dict):
        return {"bojautologin": self.token, "OnlineJudge": cookies["OnlineJudge"]}


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
            return Credential.of_json(json_str=crypto.decrypt(key, credential))
        except Exception as e:
            print(e)
            raise AuthenticationError("Failed to read the credential")

    def save(self, credential: Credential) -> None:
        key = crypto.create_key()
        util.write_file(self.__key_path(), key)
        util.write_file(
            self.__credential_path(), crypto.encrypt(key, credential.to_json())
        )
