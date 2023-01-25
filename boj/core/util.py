import os, ntpath, json
import boj.core.constant as constant
import boj.core.auth as auth
from boj.core.problem import Problem


def temp_dir():
    return str(os.getenv("HOME")) + constant.DIR


def home_url():
    return constant.BOJ_URL


def submit_url(problem_id):
    return constant.BOJ_URL + "/submit" + "/" + problem_id


def websocket_url():
    return constant.WEBSOCKET_URL


def key_file_path():
    return temp_dir() + "/" + constant.KEY_NAME


def credential_file_path():
    return temp_dir() + "/" + constant.CREDENTIAL_NAME


def convert_language_code(filetype):
    return constant.LANG_DICT[filetype]


def headers():
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    }


# File io
def read_file(path, opt):
    with open(path, opt) as file:
        data = file.read()

    return data


def write_file(path, data, opt):
    with open(path, opt) as file:
        file.write(data)


def read_credential():
    key = read_file(key_file_path(), "rb")
    credential = read_file(credential_file_path(), "rb")
    decrypted = auth.decrypt(key, credential)

    return json.loads(decrypted)


def read_problem(path):
    source = read_file(path, "r")
    id, filetype = parse_path(path)
    return Problem(id, filetype, source)


# Print
def parse_path(file_path: str):
    tokens = ntpath.basename(str(file_path)).split(".")
    id = tokens[0]
    ft = tokens[1]
    return id, ft


def clear_line():
    print("\r" + " " * 50, end="")


def print_white(s: str):
    print("\033[1m" + s + "\033[0m", end="")


def print_green(s: str):
    print("\033[92m" + "\033[1m" + s + "\033[0m", end="")


def print_red(s: str):
    print("\033[91m" + "\033[1m" + s + "\033[0m", end="")


def print_yellow(s: str):
    print("\033[33m" + "\033[1m" + s + "\033[0m", end="")


def print_magenta(s: str):
    print("\033[35m" + "\033[1m" + s + "\033[0m", end="")
