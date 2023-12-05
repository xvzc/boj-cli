import os

from boj.core import util


class Testcase:
    __test__ = False
    label: str
    data_in: str
    data_out: str

    def __init__(self, label, data_in, data_out):
        self.label = label
        self.data_in = data_in
        self.data_out = data_out

    def __repr__(self):
        return "Testcase {" + str(self.data_in) + ", " + self.data_out + "}"


class TomlTestcase:
    __test__ = False
    testcases: list[Testcase]

    def __init__(self, testcases: list[Testcase]):
        self.testcases = testcases

    @classmethod
    def read(cls, path):
        toml = util.read_toml(path=path)
        testcases = [
            Testcase(
                label=k, data_in=util.normalize(v["input"]), data_out=util.normalize(v["output"])
            )
            for k, v in toml.items()
        ]
        return TomlTestcase(testcases=testcases)

    def save(self, dir_: str):
        toml_content = self._create_toml_content()
        util.write_file(
            os.path.join(dir_, "testcase.toml"),
            bytes(toml_content, 'utf-8'),
        )

    def _create_toml_content(self):
        toml_content = ""
        for idx, val in enumerate(self.testcases):
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
