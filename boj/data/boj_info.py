import os
from pathlib import Path

from boj.core import util
from boj.core.error import IllegalStatementError, ResourceNotFoundError
import json


class BojInfo(object):
    root_dir: str
    id: str
    title: str
    filetype: str
    language: str
    source_path: str
    testcase_path: str
    checksum: str
    accepted: bool

    def __init__(
        self,
        root_dir: str,
        id_: str,
        title: str,
        filetype: str,
        language: str,
        source_path: str,
        testcase_path: str,
        checksum: str,
        accepted: bool,
    ):
        self.root_dir = root_dir
        self.id = id_
        self.title = title
        self.filetype = filetype
        self.language = language
        self.source_path = source_path
        self.testcase_path = testcase_path
        self.checksum = checksum
        self.accepted = accepted

    def get_source_path(self):
        return os.path.join(self.root_dir, self.source_path)

    def get_testcase_path(self):
        return os.path.join(self.root_dir, self.testcase_path)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "filetype": self.filetype,
            "language": self.language,
            "source_path": self.source_path,
            "testcase_path": self.testcase_path,
            "checksum": self.checksum,
            "accepted": self.accepted,
        }

    @classmethod
    def read(cls, dir: str):
        try:
            d = util.read_json(os.path.join(dir, ".boj-info.json"))
            return cls(
                root_dir=dir,
                id_=d["id"],
                title=d["title"],
                filetype=d["filetype"],
                language=d["language"],
                source_path=d["source_path"],
                testcase_path=d["testcase_path"],
                checksum=d["checksum"],
                accepted=d["accepted"],
            )
        except FileNotFoundError:
            raise IllegalStatementError(
                f"Can not find '{dir}/.boj-info.json'. "
                + "Did you run 'boj add $problem_id'?"
            )

    @classmethod
    def find_any(
        cls, ongoing_dir: str, problem_id: str, cwd=os.path.expanduser(os.getcwd())
    ):
        if problem_id:
            return cls.read(os.path.join(ongoing_dir, problem_id))
        else:
            return cls.find_upward(cwd=cwd)

    @classmethod
    def find_upward(cls, cwd=os.path.expanduser(os.getcwd())):
        try:
            boj_info_path = util.search_file_upward(
                suffix=".boj-info.json", cwd=cwd, only_dir=True
            )
            return cls.read(dir=str(Path(boj_info_path)))

        except ResourceNotFoundError:
            raise IllegalStatementError(
                "Please provide the 'problem id' "
                + "to run this command outside of problem directories"
            )

    def save(self):
        util.write_file(
            os.path.join(self.root_dir, ".boj-info.json"),
            bytes(json.dumps(self.to_dict(), indent=4, ensure_ascii=False), "utf-8"),
        )

    def __repr__(self):
        data = {
            "id": self.id,
            "title": self.title,
            "filetype": self.filetype,
            "language": self.language,
            "source_path": self.source_path,
            "testcase_path": self.testcase_path,
            "checksum": self.checksum,
            "accepted": self.accepted,
        }
        return json.dumps(data, ensure_ascii=False)
