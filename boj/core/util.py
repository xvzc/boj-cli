import json
import ntpath
import os
import yaml

from rich.console import Console

from boj.core import constant
from boj.core.config import FiletypeConfig
from boj.core.data import Solution, Testcase
from boj.core.error import ParsingConfigError, FileIOError


def convert_language_code(lang):
    lang_dict = constant.lang_dict()
    if lang not in lang_dict:
        console = Console()
        console.print(lang + " is not a supported language")

    return lang_dict[lang]


def create_dir():
    try:
        os.makedirs(constant.boj_path(), exist_ok=True)
    except OSError as e:
        raise e


def read_file(path, opt):
    try:
        if not os.path.isfile(path):
            raise FileIOError(f"{path} is not a file")

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


def read_solution(path):
    source = read_file(path, "r")
    problem_id, filetype = parse_path(path)
    return Solution(problem_id, filetype, source)


def read_runner_config(filetype):
    try:
        runner_config = read_json(constant.config_file_path()).get("filetype", None)
        if not runner_config:
            raise ParsingConfigError(
                '"filetype" property is not found in the runner config'
            )

        file_config = runner_config[filetype]

        if "default_language" not in file_config:
            raise ParsingConfigError(
                '"default_language" property is not found in the runner config'
            )

        if "run" not in file_config:
            raise ParsingConfigError('"run" property is not found in the runner config')

        return FiletypeConfig(
            default_language=file_config["default_language"],
            compile_command=file_config.get("compile", None),
            run_command=file_config["run"],
        )
    except Exception as e:
        print(e)
        raise ParsingConfigError("Error while parsing runner config.")


def parse_path(file_path: str):
    tokens = ntpath.basename(str(file_path)).split(".")
    problem_id = tokens[0]
    filetype = tokens[1]
    return problem_id, filetype


def read_testcases() -> list[Testcase]:
    testcases = read_yaml(constant.testcase_file_path())
    return [
        Testcase(data_in=testcase.get("input", ""), data_out=testcase.get("output", ""))
        for testcase in testcases
    ]


def testcases_to_yaml_content(testcases: list[Testcase]):
    yaml_content = ""
    for testcase in testcases:
        yaml_content = yaml_content + "- input: |\n"

        input_content = ""
        for line in testcase.data_in.splitlines():
            input_content = input_content + (" "*4) + line + "\n"

        yaml_content = yaml_content + input_content

        yaml_content = yaml_content + (" "*2) + "output: |\n"
        output_content = ""
        for line in testcase.data_out.splitlines():
            output_content = output_content + (" "*4) + line + "\n"

        yaml_content = yaml_content + output_content
        yaml_content = yaml_content + "\n"

    return yaml_content


def read_config_file() -> dict:
    if os.path.isfile(f"{constant.boj_path()}/config.json"):
        print("'config.json' is deprecated. Remove it and use 'config.yaml' instead.")

    if not os.path.isfile(f"{constant.boj_path()}/config.yaml"):
        print("'config.yaml' is not found. Using default values.")
        return {}

    try:
        return read_yaml(constant.config_file_path())
    except (Exception,) as e:
        return {}
