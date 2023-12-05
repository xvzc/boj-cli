from boj.core import util
from boj.data.boj_info import BojInfo


class Solution:
    def __init__(self, path, id_, language, source_code):
        self.path = path
        self.id = id_
        self.language = language
        self.source_code = source_code

    def __repr__(self):
        return (
            "Problem {"
            + str(self.id)
            + ", "
            + self.language
            + ", "
            + self.source_code
            + "}"
        )

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.language == other.filetype
            and self.source_code == other.source_code
        )

    @classmethod
    def read(cls, boj_info: BojInfo):
        source = util.read_file(boj_info.get_source_path()).decode("utf-8")
        return Solution(
            path=boj_info.get_source_path(),
            id_=boj_info.id,
            language=boj_info.language,
            source_code=source,
        )
