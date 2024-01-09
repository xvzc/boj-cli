import hashlib
import io
import json
import os
import yaml
import tomllib

from boj.core import constant
from boj.core.error import FileIOError, IllegalStatementError, ResourceNotFoundError
from pathlib import PurePath, Path


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


def file_exists(path: str):
    if os.path.isfile(path):
        return True
    return False


def read_file(path: str) -> bytes:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"'{path}' is not a file or does not exist")

    try:
        with open(path, "rb") as file:
            data = file.read()

        return data
    except Exception:
        raise FileIOError(f"Error while reading the file '{path}'")


def write_file(path: str, data: bytes):
    with open(path, "wb") as file:
        file.write(data)


def copy_file(from_path: str, to_path):
    data = read_file(path=from_path)
    write_file(path=to_path, data=data)


def read_json(path):
    return json.loads(read_file(path).decode("utf-8"))


def read_yaml(path):
    return yaml.safe_load(read_file(path).decode("utf-8"))


def read_toml(path):
    return tomllib.loads(read_file(path).decode("utf-8"))


def file_hash(path):
    return hashlib.file_digest(io.BytesIO(read_file(path)), "sha256").hexdigest()[:32]


def read_config_file(dir_: str) -> dict:
    config_file_path = os.path.join(dir_, ".boj", "config.yaml")
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


def search_file_in_parent_dirs(suffix: str, cwd=os.path.expanduser(os.getcwd())):
    cwd = PurePath(cwd)
    home = PurePath(os.path.expanduser("~"))
    while True:
        query = Path(os.path.join(cwd, suffix))
        if file_exists(str(query)):
            return str(query)

        if str(home) == str(cwd):
            raise ResourceNotFoundError(
                f"Can not find the file '{suffix}' in any of the parent directories"
            )

        cwd = cwd.parent
