import os
from typing import Optional, Type, Self

from boj.core import constant
from boj.core.error import IllegalStatementError, ResourceNotFoundError
import json

from boj.core.fs.file_search_strategy import (
    FileSearchStrategy,
    StaticSearchStrategy,
    UpwardSearchStrategy,
)
from boj.core.fs.repository import Repository, T
from boj.core.fs.serializer import Serializer
from boj.core.fs.file_object import FileMetadata, FileObject
from boj.data.config import FiletypeConfig


def _convert_language_code(lang):
    lang_dict = constant.lang_dict()
    if lang not in lang_dict:
        raise IllegalStatementError(lang + " is not a supported language")

    return lang_dict[lang]


class BojInfo(FileObject):
    def __init__(
        self,
        metadata: FileMetadata,
        id_: str,
        title: str,
        filetype: str,
        language: str,
        source_path: str,
        testcase_dir: str,
        checksum: Optional[str] = None,
        accepted: bool = False,
    ):
        super().__init__(metadata)
        self.__id = id_
        self.__title = title
        self.__filetype = filetype
        self.__language = language
        self.__source_path = source_path
        self.__testcase_dir = testcase_dir
        self.__checksum = checksum
        self.__accepted = accepted

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

    def source_path(self, abs_: bool) -> str:
        if abs_:
            return os.path.join(self.metadata.dir, self.__source_path)
        else:
            return self.__source_path

    def testcase_dir(self, abs_: bool) -> str:
        if abs_:
            return os.path.join(self.metadata.dir, self.__testcase_dir)
        else:
            return self.__testcase_dir

    @property
    def source_dir(self) -> str:
        return os.path.dirname(self.source_path(abs_=True))

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

    def __repr__(self):
        data = {
            "id": self.__id,
            "title": self.__title,
            "filetype": self.__filetype,
            "language": self.__language,
            "source_path": self.__source_path,
            "testcase_dir": self.__testcase_dir,
            "checksum": self.__checksum,
            "accepted": self.__accepted,
        }
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def of(
        cls,
        id_: int,
        title: str,
        config: FiletypeConfig,
        dir_: str,
    ) -> Type[Self]:
        return cls(
            metadata=FileMetadata.of(os.path.join(dir_, ".boj-info.json")),
            id_=str(id_),
            title=title,
            filetype=config.filetype,
            language=_convert_language_code(config.language),
            source_path=os.path.join(config.source_dir, config.filename),
            testcase_dir="testcases",
        )

    @classmethod
    def query_factory(
        cls, ongoing_dir: str, problem_id: str
    ) -> (str, FileSearchStrategy):
        if problem_id:
            return (
                ongoing_dir,
                os.path.join(str(problem_id), ".boj-info.json"),
                StaticSearchStrategy(),
            )
        else:
            return os.getcwd(), ".boj-info.json", UpwardSearchStrategy()


class BojInfoSerializer(Serializer):
    def marshal(self, raw: bytes, metadata: FileMetadata) -> BojInfo:
        data = json.loads(raw.decode("utf-8"))
        return BojInfo(
            metadata=metadata,
            id_=data["id"],
            title=data["title"],
            filetype=data["filetype"],
            language=data["language"],
            source_path=data["source_path"],
            testcase_dir=data["testcase_dir"],
            checksum=data["checksum"],
            accepted=data["accepted"],
        )

    def unmarshal(self, obj: BojInfo) -> bytes:
        data = {
            "id": obj.id,
            "title": obj.title,
            "filetype": obj.filetype,
            "language": obj.language,
            "source_path": obj.source_path(abs_=False),
            "testcase_dir": obj.testcase_dir(abs_=False),
            "checksum": obj.checksum,
            "accepted": obj.accepted,
        }
        return bytes(json.dumps(data, indent=4, ensure_ascii=False), "utf-8")


class BojInfoRepository(Repository[BojInfo]):
    def find(self, cwd: str = os.getcwd(), query: Optional[str] = None) -> BojInfo:
        try:
            path = self._search_strategy.find(query=query, cwd=cwd)
            metadata = FileMetadata.of(path)
            return self._serializer.marshal(self._file_io.read(path), metadata)
        except ResourceNotFoundError:
            raise ResourceNotFoundError(
                "Can not find '.boj-info.json'. did you run 'boj add $problem_id'?"
            )

    def save(self, obj: T) -> None:
        self._file_io.write(self._serializer.unmarshal(obj), obj.metadata.path)
