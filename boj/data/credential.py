import json
import os
from typing import Optional

from boj.core import crypto
from boj.core.error import ResourceNotFoundError, AuthenticationError

from boj.core.fs.file_object import FileObject, FileMetadata
from boj.core.fs.repository import Repository, T
from boj.core.fs.serializer import Serializer


class Credential(FileObject):
    def __init__(self, metadata: FileMetadata, username: str, token: str):
        super().__init__(metadata)
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

    def make_session_cookies(self, cookies: dict):
        return {"bojautologin": self.token, "OnlineJudge": cookies["OnlineJudge"]}


class CredentialSerializer(Serializer[Credential]):
    def marshal(self, raw: bytes, metadata: FileMetadata) -> Credential:
        j = json.loads(raw.decode("utf-8"))
        return Credential(
            metadata=metadata,
            username=j["username"],
            token=j["token"],
        )

    def unmarshal(self, obj: Credential) -> bytes:
        j = {
            "username": obj.username,
            "token": obj.token,
        }
        return bytes(json.dumps(j, sort_keys=True, indent=4), "utf-8")


class CredentialRepository(Repository[Credential]):
    def find(self, cwd: str = os.getcwd(), query: Optional[str] = None) -> T:
        try:
            credential_path = self._search_strategy.find(cwd, "credential")
            key_path = self._search_strategy.find(cwd, "key")
            key = self._file_io.read(key_path)
            cipher_text = self._file_io.read(credential_path)
            plain_text = crypto.decrypt(key, cipher_text)
            return self._serializer.marshal(
                raw=plain_text,
                metadata=FileMetadata.of(credential_path),
            )
        except ResourceNotFoundError:
            raise AuthenticationError(
                "Failed to load credential. Did you run 'boj login'?"
            )

    def save(self, obj: Credential) -> None:
        plain = self._serializer.unmarshal(obj=obj)
        key = crypto.create_key()
        cipher = crypto.encrypt(key, plain)
        self._file_io.write(cipher, obj.metadata.path)
        self._file_io.write(key, os.path.join(obj.metadata.dir, "key"))
