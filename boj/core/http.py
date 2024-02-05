from typing import Optional, Type

import requests
from requests import Response

from boj.core.error import HttpError
from abc import ABCMeta, abstractmethod

from boj.core.html import HtmlParser, HtmlParser


class HttpRequest(metaclass=ABCMeta):
    @abstractmethod
    def url(self) -> str:
        pass

    @abstractmethod
    def headers(self) -> Optional[dict]:
        pass

    @abstractmethod
    def cookies(self) -> Optional[dict]:
        pass


class RequestWithParams(HttpRequest, metaclass=ABCMeta):

    @abstractmethod
    def params(self) -> Optional[dict]:
        pass


class RequestWithBody(HttpRequest, metaclass=ABCMeta):
    @abstractmethod
    def data(self) -> Optional[dict]:
        pass


class HttpResponse(metaclass=ABCMeta):
    def __init__(self, response: Response):
        self.__raw = response
        self.__cookies = response.cookies.get_dict()

    @property
    def raw(self):
        return self.__raw

    @property
    def cookies(self):
        return self.__cookies


class HtmlResponse(HttpResponse):
    def __init__(self, response: Response):
        super().__init__(response)
        self.__html = response.text

    @property
    def html(self) -> str:
        return self.__html


class JsonResponse(HttpResponse):
    def __init__(self, response: Response):
        super().__init__(response)
        self.__json = response.json()

    @property
    def json(self) -> dict:
        return self.__json


def get(request: RequestWithParams) -> Response:
    try:
        res = requests.get(
            url=request.url(),
            headers=request.headers(),
            cookies=request.cookies(),
            params=request.params(),
        )
        res.raise_for_status()
        return res
    except requests.exceptions.RequestException as e:
        print(e)
        raise HttpError(f"GET {request.url}")


def post(request: RequestWithBody) -> Response:
    try:
        res = requests.post(
            url=request.url(),
            headers=request.headers(),
            cookies=request.cookies(),
            data=request.data(),
        )
        res.raise_for_status()
        return res
    except requests.exceptions.RequestException as e:
        print(e)
        raise HttpError(f"POST {request.url}")
