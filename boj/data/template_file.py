from boj.core import util
import os


class TemplateFile:
    __test__ = False

    def __init__(self, content):
        self.__content = content

    @property
    def content(self):
        return self.__content

    @classmethod
    def read_file(cls, path: str):
        try:
            content = bytes.decode(
                util.read_file(os.path.expanduser(path)), encoding="utf-8"
            )
            return cls(content=content)
        except FileNotFoundError as e:
            raise e

    def save(self, path: str):
        util.write_file(path, bytes(self.__content, "utf-8"))
