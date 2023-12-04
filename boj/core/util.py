import json
import ntpath
import os
import yaml
import tomllib

from boj.core import constant
from boj.data.testcase import Testcase
from boj.data.solution import Solution
from boj.core.error import FileIOError, IllegalStatementError, ResourceNotFoundError
from pathlib import PurePath


def convert_language_code(lang):
    lang_dict = constant.lang_dict()
    if lang not in lang_dict:
        raise IllegalStatementError(lang + " is not a supported language")

    return lang_dict[lang]


def create_temp_dir():
    try:
        os.makedirs(constant.boj_dir_path(), exist_ok=True)
    except OSError as e:
        raise e


def file_exists(path):
    if os.path.isfile(path):
        return True
    return False


def read_file(path, opt):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"'{path}' is not a file or does not exist")

    try:
        with open(path, opt) as file:
            data = file.read()

        return data
    except Exception:
        raise FileIOError(f"Error while reading the file '{path}'")


def write_file(path, data, opt):
    with open(path, opt) as file:
        file.write(data)


def copy_file(from_, to):
    data = read_file(path=from_, opt="r")
    write_file(path=to, data=data, opt="w")


def read_json(path):
    f = read_file(path, "r")
    return json.loads(f)


def read_yaml(path):
    stream = read_file(path, "r")
    return yaml.safe_load(stream)


def read_toml(path):
    stream = read_file(path, "r")
    return tomllib.loads(stream)


def read_config_file(dir_: str) -> dict:
    config_file_path = f"{dir_}/.boj/config.yaml"
    if not os.path.isfile(config_file_path):
        print("'config.yaml' is not found. Using default values.")
        return {}

    try:
        return read_yaml(config_file_path)
    except (Exception,) as e:
        return {}


def normalize(s: str):
    s = s.rstrip()
    normalized_text = "\n".join([line.rstrip() for line in s.splitlines()])
    return normalized_text


def backtrace_dir(name: str):
    cwd = PurePath(os.path.expanduser(os.getcwd()))
    home = PurePath(os.path.expanduser("~"))
    while True:
        if os.path.isdir(f"{str(cwd)}/{name}"):
            return str(cwd)

        if str(home) == str(cwd):
            raise ResourceNotFoundError(f"Can not find the directory '{name}' in any of the parent directories")

        cwd = cwd.parent


def search_file_in_parent_dirs(suffix: str, cwd=os.path.expanduser(os.getcwd())):
    cwd = PurePath(cwd)
    home = PurePath(os.path.expanduser("~"))
    while True:
        query = f"{str(cwd)}/{suffix}"
        if file_exists(query):
            return str(query)

        if str(home) == str(cwd):
            raise ResourceNotFoundError(f"Can not find the file '{suffix}' in any of the parent directories")

        cwd = cwd.parent
