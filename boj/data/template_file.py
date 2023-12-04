from boj.core import util
import os


class TemplateFile:
    __test__ = False
    content: str

    def __init__(self, content):
        self.content = content

    @classmethod
    def read_file(cls, path: str):
        try:
            content = util.read_file(os.path.expanduser(path), "r")
            return cls(content=content)
        except FileNotFoundError as e:
            raise e

    def save(self, path: str):
        util.write_file(path, self.content, "w")
