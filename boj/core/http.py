import requests
from requests import Response

from boj.core.error import HttpError
from abc import ABCMeta


class HttpRequest:
    def __init__(
        self,
        url: str,
        headers: dict = None,
        cookies: dict = None,
        data: dict = None,
    ):
        self.__url = url
        self.__headers = headers
        self.__cookies = cookies
        self.__data = data

    @property
    def url(self) -> str:
        return self.__url

    @property
    def headers(self) -> dict:
        return self.__headers

    @property
    def cookies(self) -> dict:
        return self.__cookies

    @property
    def data(self) -> dict:
        return self.__data


class HttpEntity(metaclass=ABCMeta):
    def __init__(self, response: Response):
        self.__response = response
        self.__cookies = response.cookies.get_dict()

    @property
    def response(self):
        return self.__response

    @property
    def cookies(self):
        return self.__cookies

    @classmethod
    def get(cls, request: HttpRequest):
        try:
            res = requests.get(
                url=request.url,
                headers=request.headers,
                cookies=request.cookies,
            )
            res.raise_for_status()
            return cls(res)
        except requests.exceptions.RequestException as e:
            print(e)
            raise HttpError(f"GET {request.url}")

    @classmethod
    def post(cls, request: HttpRequest):
        try:
            res = requests.post(
                url=request.url,
                headers=request.headers,
                cookies=request.cookies,
                data=request.data,
            )
            res.raise_for_status()
            return cls(res)
        except requests.exceptions.RequestException as e:
            print(e)
            raise HttpError(f"POST {request.url}")


class Page(HttpEntity):
    def __init__(self, response: Response):
        super().__init__(response)
        self.__html = response.text

    @property
    def html(self) -> str:
        return self.__html


class Api(HttpEntity):
    def __init__(self, response: Response):
        super().__init__(response)
        self.__json = response.json()

    @property
    def json(self) -> str:
        return self.__json
