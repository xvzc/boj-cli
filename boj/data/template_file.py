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
            content = bytes.decode(
                util.read_file(os.path.expanduser(path)),
                encoding="utf-8"
            )
            return cls(content=content)
        except FileNotFoundError as e:
            raise e

    def save(self, path: str):
        util.write_file(path, bytes(self.content, 'utf-8'))
