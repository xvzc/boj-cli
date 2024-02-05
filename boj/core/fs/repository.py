import hashlib
import io
import os
from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Optional

from boj.core.fs.file_object import FileObject, TextFile, FileMetadata
from boj.core.fs.file_search_strategy import FileSearchStrategy
from boj.core.fs.file_io import FileIO
from boj.core.fs.serializer import Serializer

T = TypeVar("T", bound=FileObject)


class ReadOnlyRepository(Generic[T], metaclass=ABCMeta):
    def __init__(
        self,
        file_io: FileIO,
        search_strategy: FileSearchStrategy,
        serializer: Serializer[T],
    ) -> None:
        self._file_io = file_io
        self._search_strategy = search_strategy
        self._serializer = serializer

    @property
    def search_strategy(self) -> FileSearchStrategy:
        return self._search_strategy

    @search_strategy.setter
    def search_strategy(self, search_strategy: FileSearchStrategy):
        self._search_strategy = search_strategy

    @abstractmethod
    def find(self, cwd: str = os.getcwd(), query: Optional[str] = None) -> T:
        pass

    def hash(self, obj: T):
        raw = self._serializer.unmarshal(obj)
        digest = hashlib.file_digest(io.BytesIO(raw), "sha256")
        return digest.hexdigest()[:32]


class Repository(ReadOnlyRepository, Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def save(self, obj: T) -> None:
        pass

    def copy(self, obj: T, dest: str) -> None:
        self._file_io.write(self._serializer.unmarshal(obj), dest)


class TextFileRepository(Repository[TextFile]):
    def find(self, cwd: str = os.getcwd(), query: Optional[str] = None) -> TextFile:
        path = self._search_strategy.find(query=query, cwd=cwd)
        metadata = FileMetadata.of(path)
        return self._serializer.marshal(self._file_io.read(path), metadata)

    def save(self, obj: TextFile) -> None:
        self._file_io.write(self._serializer.unmarshal(obj), obj.metadata.path)
