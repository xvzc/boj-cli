import os

from boj.core import util


class Testcase:
    __test__ = False

    def __init__(self, label, input_, output):
        self.__label = label
        self.__input = input_
        self.__output = output

    @property
    def input(self):
        return self.__input

    @property
    def output(self):
        return self.__input

    @property
    def label(self):
        return self.__label

    def __repr__(self):
        return "Testcase {" + str(self.__input) + ", " + self.__output + "}"


class TestcaseIO:
    __dir: str

    def __init__(self, dir_: str):
        self.__dir = dir_

    def get_dir(self) -> str:
        return self.__dir

    def find_all(self) -> list[Testcase]:
        pass

    def find_one(self) -> Testcase:
        pass

    def save_all(self, testcase: list[Testcase]) -> None:
        pass

    def save_one(self, testcase: Testcase) -> None:
        pass


class Testcases:
    def __init__(self, testcases: list[Testcase]):
        self.__testcases = testcases

    @property
    def testcases(self) -> list[Testcase]:
        return self.__testcases

    @classmethod
    def read(cls, path):
        toml = util.read_toml(path=path)
        testcases = [
            Testcase(
                label=k,
                input_=util.normalize(v["input"]),
                output=util.normalize(v["output"]),
            )
            for k, v in toml.items()
        ]
        return Testcases(testcases=testcases)

    def save(self, dir_: str):
        toml_content = self._create_toml_content()
        util.write_file(
            os.path.join(dir_, "testcase.toml"),
            bytes(toml_content, "utf-8"),
        )

    def _create_toml_content(self):
        toml_content = ""
        for idx, val in enumerate(self.__testcases):
            content = [
                f"[{idx + 1}]",
                'input = """',
                val.input,
                '"""',
                "",
                'output = """',
                val.output,
                '"""',
                "\n",
            ]
            toml_content += "\n".join(content)

        return toml_content
