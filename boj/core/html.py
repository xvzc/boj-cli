from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class HtmlParser(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def find(self, html: str) -> T:
        pass
