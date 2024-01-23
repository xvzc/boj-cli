import os
from pathlib import Path

from boj.core import util
from boj.core.error import IllegalStatementError, ResourceNotFoundError
import json


class BojInfo(object):
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
        self.__root_dir = root_dir
        self.__id = id_
        self.__title = title
        self.__filetype = filetype
        self.__language = language
        self.__source_path = source_path
        self.__testcase_path = testcase_path
        self.__checksum = checksum
        self.__accepted = accepted

    @property
    def root_dir(self) -> str:
        return self.__root_dir

    @property
    def id(self) -> str:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def filetype(self) -> str:
        return self.__filetype

    @property
    def language(self) -> str:
        return self.__language

    @property
    def source_path(self) -> str:
        return os.path.join(self.root_dir, self.__source_path)

    @property
    def testcase_path(self) -> str:
        return os.path.join(self.root_dir, self.__testcase_path)

    @property
    def checksum(self) -> str:
        return self.__checksum

    @checksum.setter
    def checksum(self, checksum: str):
        self.__checksum = checksum

    @property
    def accepted(self) -> bool:
        return self.__accepted

    @accepted.setter
    def accepted(self, accepted: bool):
        self.__accepted = accepted

    def to_dict(self):
        return {
            "id": self.__id,
            "title": self.__title,
            "filetype": self.__filetype,
            "language": self.__language,
            "source_path": self.__source_path,
            "testcase_path": self.__testcase_path,
            "checksum": self.__checksum,
            "accepted": self.__accepted,
        }

    @classmethod
    def read(cls, dir_: str):
        try:
            d = util.read_json(os.path.join(dir_, ".boj-info.json"))
            return cls(
                root_dir=dir_,
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
                f"Can not find '{dir_}/.boj-info.json'. "
                + "Did you run 'boj add $problem_id'?"
            )

    @classmethod
    def find_any(
        cls,
        ongoing_dir: str,
        problem_id: str,
        cwd=os.path.expanduser(os.getcwd()),
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
            return cls.read(dir_=str(Path(boj_info_path)))

        except ResourceNotFoundError:
            raise IllegalStatementError(
                "Please provide the 'problem id' "
                + "to run this command outside of problem directories"
            )

    def save(self):
        util.write_file(
            os.path.join(self.__root_dir, ".boj-info.json"),
            bytes(json.dumps(self.to_dict(), indent=4, ensure_ascii=False), "utf-8"),
        )

    def __repr__(self):
        data = {
            "id": self.__id,
            "title": self.__title,
            "filetype": self.__filetype,
            "language": self.__language,
            "source_path": self.__source_path,
            "testcase_path": self.__testcase_path,
            "checksum": self.__checksum,
            "accepted": self.__accepted,
        }
        return json.dumps(data, ensure_ascii=False)
