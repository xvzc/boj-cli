import os

from boj.core.fs.file_object import TextFile, FileMetadata


def normalize(s: str):
    s = s.rstrip()
    normalized_text = "\n".join([line.rstrip() for line in s.splitlines()])
    return normalized_text


class Testcase:
    __test__ = False

    def __init__(self, label: str, input_: str, output: str):
        self.__label = label
        self.__input = input_
        self.__output = output

    @property
    def input(self):
        return self.__input

    @property
    def output(self):
        return self.__output

    @property
    def label(self):
        return self.__label

    def __repr__(self):
        return "Testcase {" + self.input + ", " + self.output + "}"

    def compare(self, stdout: str):
        return normalize(self.output) == normalize(stdout)

    def to_text_files(self, dir_: str) -> (TextFile, TextFile):
        input_ = TextFile(
            FileMetadata.of(os.path.join(dir_, self.label, "input.txt")),
            content=self.input,
        )
        output = TextFile(
            FileMetadata.of(os.path.join(dir_, self.label, "output.txt")),
            content=self.output,
        )
        return input_, output

    @classmethod
    def of(cls, label: str, input_: TextFile, output: TextFile):
        return cls(label=label, input_=input_.content, output=output.content)
