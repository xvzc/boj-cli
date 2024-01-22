from boj.core import util
from boj.data.boj_info import BojInfo


class Solution:
    def __init__(self, path, id_, language, source_code):
        self.__path = path
        self.__id = id_
        self.__language = language
        self.__source_code = source_code

    @property
    def path(self):
        return self.__path

    @property
    def id(self):
        return self.__id

    @property
    def language(self):
        return self.__language

    @property
    def source_code(self):
        return self.__source_code

    def __repr__(self):
        return (
            "Problem {"
            + str(self.__id)
            + ", "
            + self.__language
            + ", "
            + self.__source_code
            + "}"
        )

    def __eq__(self, other):
        return (
            self.__id == other.__id
            and self.__language == other.__filetype
            and self.__source_code == other.__source_code
        )

    @classmethod
    def read(cls, boj_info: BojInfo):
        source = util.read_file(boj_info.source_path).decode("utf-8")
        return Solution(
            path=boj_info.source_path,
            id_=boj_info.id,
            language=boj_info.language,
            source_code=source,
        )
