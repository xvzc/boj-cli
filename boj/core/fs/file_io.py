import os
from abc import ABCMeta, abstractmethod

from boj.core.error import FileIOError
from boj.core.fs.util import mkdir


class FileIO(metaclass=ABCMeta):
    @abstractmethod
    def read(self, path: str) -> bytes:
        pass

    @abstractmethod
    def write(self, raw: bytes, path: str) -> None:
        pass


class GeneralFileIO(FileIO):
    def read(self, path: str) -> bytes:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"'{path}' is not a file or does not exist")

        try:
            with open(path, "rb") as file:
                data = file.read()

            return data
        except Exception:
            raise FileIOError(f"Error while reading the file '{path}'")

    def write(self, raw: bytes, path: str) -> None:
        mkdir(os.path.dirname(path))
        with open(path, "wb") as file:
            file.write(raw)
