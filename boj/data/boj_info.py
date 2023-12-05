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
    def read(cls, problem_root: str):
        d = util.read_json(os.path.join(problem_root, ".boj-info.json"))
        return cls(
            root_dir=problem_root,
            id_=d["id"],
            title=d["title"],
            filetype=d["filetype"],
            language=d["language"],
            source_path=d["source_path"],
            testcase_path=d["testcase_path"],
            checksum=d["checksum"],
            accepted=d["accepted"],
        )

    @classmethod
    def find_any(
        cls, problem_dir: str, problem_id: str, cwd=os.path.expanduser(os.getcwd())
    ):
        try:
            if problem_id:
                return cls.read(os.path.join(problem_dir, problem_id))
            else:
                boj_info_suffix = ".boj-info.json"
                boj_info_path = util.search_file_in_parent_dirs(
                    boj_info_suffix, cwd=cwd
                )
                return cls.read(
                    problem_root=str(Path(boj_info_path.replace(boj_info_suffix, "")))
                )

        except FileNotFoundError:
            raise IllegalStatementError(
                f"Can not find the problem {problem_id} (.boj-info.json). Did you run 'boj add'?"
            )
        except ResourceNotFoundError:
            raise IllegalStatementError(
                "Please provide the 'problem id' to run this command outside of problem directories"
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
