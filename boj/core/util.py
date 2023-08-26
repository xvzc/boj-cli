import os, ntpath, json, time, yaml

from rich.console import Console

from boj.core import property
from boj.core.data import Solution, Testcase, RunnerConfig
from boj.core.error import ParsingConfigError, FileIOError


def convert_language_code(lang):
    lang_dict = property.lang_dict()
    if lang not in lang_dict:
        console = Console()
        console.print(lang + " is not a supported language")

    return lang_dict[lang]


def create_dir():
    try:
        os.makedirs(property.boj_path(), exist_ok=True)
        os.makedirs(property.drivers_dir(), exist_ok=True)
    except OSError as e:
        raise e


def read_file(path, opt):
    try:
        if not os.path.isfile(path):
            raise FileIOError(f'{path} is not a file')

        with open(path, opt) as file:
            data = file.read()

        return data
    except Exception:
        raise FileIOError(f'Error while reading file. {path}')


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
        runner_config = read_json(property.runner_config_file_path()).get('filetype', None)
        if not runner_config:
            raise ParsingConfigError('"filetype" property is not found in the runner config')

        file_config = runner_config[filetype]

        if 'default_language' not in file_config:
            raise ParsingConfigError('"default_language" property is not found in the runner config')

        if 'run' not in file_config:
            raise ParsingConfigError('"run" property is not found in the runner config')

        return RunnerConfig(
            default_language=file_config['default_language'],
            compile_command=file_config.get('compile', None),
            run_command=file_config['run'],
        )
    except Exception as e:
        print(e)
        raise ParsingConfigError('Error while parsing runner config.')


def parse_path(file_path: str):
    tokens = ntpath.basename(str(file_path)).split(".")
    problem_id = tokens[0]
    filetype = tokens[1]
    return problem_id, filetype


def read_testcases() -> list[Testcase]:
    testcases = read_yaml(property.testcase_file_path())
    return [
        Testcase(
            data_in=testcase.get('input', ''),
            data_out=testcase.get('output', '')
        ) for testcase in testcases
    ]


def testcases_to_yaml(testcases: list[Testcase]):
    def str_presenter(dumper, data):
        if isinstance(data, str) and data.startswith(property.salt()):
            data = data.replace(property.salt(), "")
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")

        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    yaml.add_representer(str, str_presenter)
    yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

    yaml_testcases = yaml.dump([t.to_dict() for t in testcases], indent=2)
    return yaml_testcases.replace("- input", "\n- input").lstrip()
