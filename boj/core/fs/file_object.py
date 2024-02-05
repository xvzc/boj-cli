import os
from pathlib import Path


class FileMetadata:
    def __init__(self, path: str, dir_: str, name: str):
        self.__path = path
        self.__dir = dir_
        self.__name = name

    @classmethod
    def of(cls, path: str):
        path = Path(path)
        return cls(str(path), dir_=os.path.dirname(path), name=path.name)

    @property
    def path(self):
        return self.__path

    @property
    def dir(self):
        return self.__dir

    @property
    def name(self):
        return self.__name


class FileObject:
    def __init__(self, metadata: FileMetadata):
        self.__metadata = metadata

    @property
    def metadata(self) -> FileMetadata:
        return self.__metadata


class TextFile(FileObject):
    def __init__(self, metadata: FileMetadata, content: str):
        super().__init__(metadata)
        self.__metadata = metadata
        self.__content = content

    @property
    def content(self):
        return self.__content
