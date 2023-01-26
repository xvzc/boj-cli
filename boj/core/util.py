import os, ntpath, json

from rich.console import Console
import boj.core.constant as constant
import boj.core.language as language
import boj.core.auth as auth
from boj.core.problem import Problem


def temp_dir():
    return str(os.getenv("HOME")) + constant.DIR

def config_file_path():
    return str(os.getenv("HOME")) + constant.DIR + "/" + constant.CONFIG_FILE_NAME

def key_file_path():
    return temp_dir() + "/" + constant.KEY_FILE_NAME


def credential_file_path():
    return temp_dir() + "/" + constant.CREDENTIAL_FILE_NAME

def home_url():
    return constant.BOJ_URL


def submit_url(problem_id):
    return home_url() + "/submit" + "/" + str(problem_id)


def problem_url(problem_id):
    return home_url() + "/problem" + "/" + str(problem_id)


def websocket_url():
    return constant.WEBSOCKET_URL



def convert_language_code(language_name):
    if language_name not in language.LANGUAGE_DICT:
        console = Console()
        console.print(language_name + " is not a supported language")


    return language.LANGUAGE_DICT[language_name]


def headers():
    return {"User-Agent": constant.USER_AGENT}


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
