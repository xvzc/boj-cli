import os, ntpath, json, time, yaml

from rich.console import Console

import boj.core
import boj.core.auth as auth
from boj.core.solution import Solution


def temp_dir():
    return str(os.getenv("HOME")) + boj.core.DIR


def config_file_path():
    return str(os.getenv("HOME")) + boj.core.DIR + "/" + boj.core.CONFIG_FILE_NAME


def key_file_path():
    return temp_dir() + "/" + boj.core.KEY_FILE_NAME


def credential_file_path():
    return temp_dir() + "/" + boj.core.CREDENTIAL_FILE_NAME


def home_url():
    return boj.core.BOJ_URL


def submit_url(problem_id):
    return home_url() + "/submit" + "/" + str(problem_id)


def problem_url(problem_id):
    return home_url() + "/problem" + "/" + str(problem_id)


def websocket_url():
    return boj.core.WEBSOCKET_URL


def solvedac_home_url():
    return boj.core.SOVEDAC_URL


def solvedac_search_url():
    return solvedac_home_url() + "/search"


def solvedac_search_problem_url():
    return solvedac_search_url() + "/problem"


def convert_language_code(language_name):
    if language_name not in boj.core.LANGUAGE_DICT:
        console = Console()
        console.print(language_name + " is not a supported language")

    return boj.core.LANGUAGE_DICT[language_name]


def headers():
    return {"User-Agent": boj.core.USER_AGENT}


# File io
def read_file(path, opt):
    if not os.path.isfile(path):
        return None

    with open(path, opt) as file:
        data = file.read()

    return data


def write_file(path, data, opt):
    with open(path, opt) as file:
        file.write(data)


def read_credential():
    key = read_file(key_file_path(), "rb")
    if not key:
        return None

    credential = read_file(credential_file_path(), "rb")
    if not credential:
        return None

    decrypted = auth.decrypt(key, credential)

    return json.loads(decrypted)


def read_config():
    config = None
    try:
        f = read_file(config_file_path(), "r")
        config = json.loads(f)
    except:
        return None

    return config


def read_testcase():
    testcases = None
    try:
        stream = read_file("./testcase.yaml", "r")
        testcases = yaml.safe_load(stream)
        return testcases
    except:
        return None


def read_solution(path):
    source = read_file(path, "r")
    problem_id, filetype = parse_path(path)
    time.sleep(0.3)
    return Solution(problem_id, filetype, source)


# Print
def parse_path(file_path: str):
    tokens = ntpath.basename(str(file_path)).split(".")
    id = tokens[0]
    ft = tokens[1]
    return id, ft
