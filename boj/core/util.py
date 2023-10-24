import json
import ntpath
import os
import yaml
import tomllib

from boj.core import constant
from boj.core.data import Solution, Testcase
from boj.core.error import FileIOError, IllegalStatementError
from boj.core import util


def convert_language_code(lang):
    lang_dict = constant.lang_dict()
    if lang not in lang_dict:
        raise IllegalStatementError(lang + " is not a supported language")

    return lang_dict[lang]


def create_boj_dir():
    try:
        os.makedirs(constant.boj_dir_path(), exist_ok=True)
        os.makedirs(constant.template_dir_path(), exist_ok=True)
    except OSError as e:
        raise e


def file_exists(path):
    if os.path.isfile(path):
        return True
    return False


def read_file(path, opt):
    try:
        if not os.path.isfile(path):
            raise FileIOError(f"'{path}' is not a file or doesn't exist")

        with open(path, opt) as file:
            data = file.read()

        return data
    except Exception:
        raise FileIOError(f"Error while reading file. {path}")


def write_file(path, data, opt):
    with open(path, opt) as file:
        file.write(data)


def read_json(path):
    f = read_file(path, "r")
    return json.loads(f)


def read_yaml(path):
    stream = read_file(path, "r")
    return yaml.safe_load(stream)


def read_toml(path):
    stream = read_file(path, "r")
    return tomllib.loads(stream)


def read_solution(path):
    source = read_file(path, "r")
    problem_id, filetype = parse_path(path)
    return Solution(problem_id, filetype, source)


def parse_path(file_path: str):
    tokens = ntpath.basename(str(file_path)).split(".")
    problem_id = tokens[0]
    filetype = tokens[1]
    return problem_id, filetype


def read_testcases() -> list[Testcase]:
    testcases = read_toml(constant.testcase_file_path())
    return [
        Testcase(label=k, data_in=normalize(v["input"]), data_out=normalize(v["output"]))
        for k, v in testcases.items()
    ]


def testcases_to_yaml_content(testcases: list[Testcase]):
    yaml_content = ""
    for testcase in testcases:
        yaml_content = yaml_content + "- input: |2\n"

        input_content = ""
        for line in testcase.data_in.splitlines():
            input_content = input_content + (" " * 4) + line + "\n"

        yaml_content = yaml_content + input_content

        yaml_content = yaml_content + (" " * 2) + "output: |2\n"
        output_content = ""
        for line in testcase.data_out.splitlines():
            output_content = output_content + (" " * 4) + line + "\n"

        yaml_content = yaml_content + output_content
        yaml_content = yaml_content + "\n"

    return yaml_content


def testcases_to_toml_content(testcases: list[Testcase]):
    toml_content = ""
    for idx, val in enumerate(testcases):
        content = [
            f"[{idx + 1}]",
            'input = """',
            val.data_in,
            '"""',
            "",
            'output = """',
            val.data_out,
            '"""',
            "\n",
        ]
        toml_content += "\n".join(content)

    return toml_content


def read_template(lang) -> str:
    return read_file(f"{constant.template_dir_path()}/template.{lang}", "r")


def read_config_file() -> dict:
    if os.path.isfile(f"{constant.boj_dir_path()}/config.json"):
        print("'config.json' is deprecated. Remove it and use 'config.yaml' instead.")

    if not os.path.isfile(f"{constant.boj_dir_path()}/config.yaml"):
        print("'config.yaml' is not found. Using default values.")
        return {}

    try:
        return read_yaml(constant.config_file_path())
    except (Exception,) as e:
        return {}


def normalize(s: str):
    s = s.rstrip()
    normalized_text = "\n".join([line.rstrip() for line in s.splitlines()])
    return normalized_text
