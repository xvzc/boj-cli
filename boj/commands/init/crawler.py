from bs4 import BeautifulSoup
import yaml
import requests

from boj.core import util

from boj.core import SALT


# Returns markdown
def query_problem(problem_id):
    res = requests.get(util.problem_url(problem_id), headers=util.headers())
    return res.text


def extract_testcases(html):
    soup = BeautifulSoup(html, "html.parser")
    sample_data = soup.select("pre.sampledata")

    inputs = []
    outputs = []
    for data in sample_data:
        text = data.text

        if "input" in str(data.get("id", "")):
            text = text.rstrip()
            inputs.append(text.rstrip())

        if "output" in str(data.get("id", "")):
            text = text.rstrip()
            outputs.append(text.rstrip())

    testcases = {}
    for i in range(len(inputs)):
        test_name = "test" + str(i + 1)
        testcases[test_name] = {}

        # Prepend some complicated string just in case that testcases contain
        # such strings like input.*, output.*, or run[0-9]

        if inputs[i]:
            testcases[test_name]["input"] = SALT + inputs[i] + "\n"
        if outputs[i]:
            testcases[test_name]["output"] = SALT + outputs[i] + "\n"

    return testcases


def str_presenter(dumper, data):
    if isinstance(data, str) and data.startswith(SALT):
        data = data.replace(SALT, "")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")

    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def yamlify_testcases(testcases):
    yaml.add_representer(str, str_presenter)
    yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

    yaml_testcases = yaml.dump(testcases, indent=2)
    return yaml_testcases
