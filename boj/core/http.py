import requests

from boj.core.error import HttpError


def get(url, headers=None, cookies=None):
    try:
        res = requests.get(url=url, headers=headers, cookies=cookies)
        res.raise_for_status()
        return res
    except requests.exceptions.RequestException as e:
        print(e)
        raise HttpError(f"GET {url}")


def post(url, headers=None, cookies=None, data=None):
    try:
        res = requests.post(url=url, headers=headers, cookies=cookies, data=data)
        res.raise_for_status()
        return res
    except requests.exceptions.RequestException as e:
        raise HttpError(f"POST {url}")
