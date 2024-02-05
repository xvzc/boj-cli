import os
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Optional

from boj.core.error import ResourceNotFoundError
from boj.core.fs.util import file_exists


class FileSearchStrategy(metaclass=ABCMeta):
    @abstractmethod
    def find(self, cwd: str, query: str) -> Optional[str]:
        pass


class UpwardSearchStrategy(FileSearchStrategy):
    def find(
        self,
        cwd: str,
        query: str,
    ) -> Optional[str]:
        path = Path(cwd)
        home = Path(os.path.expanduser("~"))
        while True:
            cur_path = Path(os.path.join(path, query))
            if file_exists(str(cur_path)):
                return str(cur_path)

            if str(home) == str(path):
                raise ResourceNotFoundError(f"File Not Found: {query}")

            path = path.parent


class StaticSearchStrategy(FileSearchStrategy):
    def find(self, cwd: str, query: str) -> Optional[str]:
        path = os.path.join(cwd, query)
        if file_exists(path):
            return path
        else:
            raise ResourceNotFoundError(f"File Not Found: {query}")
