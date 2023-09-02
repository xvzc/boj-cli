from enum import Enum

import requests

from boj.core.error import HttpError


def get(url, headers=None):
    try:
        res = requests.get(url=url, headers=headers)
        res.raise_for_status()
        return res
    except requests.exceptions.RequestException as e:
        print(e)
        raise HttpError(f"GET {url}")


def post(url, headers, data):
    try:
        res = requests.get(url=url, headers=headers, data=data)
        res.raise_for_status()
        return res
    except requests.exceptions.RequestException as e:
        raise HttpError(f"POST {url}")
