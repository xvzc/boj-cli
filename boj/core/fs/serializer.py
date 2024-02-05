from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from boj.core.fs.file_object import FileMetadata, FileObject, TextFile

T = TypeVar("T", bound=FileObject)


class Serializer(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def marshal(self, raw: bytes, metadata: FileMetadata) -> T:
        pass

    @abstractmethod
    def unmarshal(self, obj: T) -> bytes:
        pass


class TextFileSerializer(Serializer[TextFile]):
    def marshal(self, raw: bytes, metadata: FileMetadata) -> TextFile:
        return TextFile(metadata=metadata, content=raw.decode("utf-8"))

    def unmarshal(self, obj: TextFile) -> bytes:
        return bytes(obj.content, "utf-8")
