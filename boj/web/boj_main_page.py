from typing import Optional

from boj.core import constant
from boj.core.http import RequestWithParams


class BojMainPageRequest(RequestWithParams):
    def url(self) -> str:
        return constant.boj_main_url()

    def headers(self) -> Optional[dict]:
        return constant.default_headers()

    def cookies(self) -> Optional[dict]:
        return None

    def params(self) -> Optional[dict]:
        return None
