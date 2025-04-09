import dataclasses
import os

from rich.console import Console

from boj.core.command import Command
from boj.core.error import IllegalStatementError, FatalError
from boj.core.fs.file_object import FileMetadata, TextFile
from boj.core.fs.file_search_strategy import StaticSearchStrategy, UpwardSearchStrategy
from boj.core.fs.repository import ReadOnlyRepository, Repository
from boj.data.boj_info import BojInfo
from boj.data.config import Config


def _open_files(command: str, input_: TextFile, output: TextFile):
    command = " ".join(
        [
            command,
            input_.metadata.path,
            output.metadata.path,
        ]
    )
    os.system(command)


@dataclasses.dataclass
class CaseCommand(Command):
    console: Console
    config_repository: ReadOnlyRepository[Config]
    boj_info_repository: Repository[BojInfo]
    text_file_repository: Repository[TextFile]

    def execute(self, args):
        config = self.config_repository.find()
        if not config.general.editor_command:
            raise FatalError("'config.general.editor_command' is not specified")

        self.boj_info_repository.search_strategy = (
            StaticSearchStrategy() if args.problem_id else UpwardSearchStrategy()
        )
        cwd = config.workspace.search_dir(args.problem_id)
        boj_info = self.boj_info_repository.find(cwd, ".boj-info.json")

        tc_dir = boj_info.testcase_dir(abs_=True)
        if args.new:
            new_id = "1"
            for testcase_id in sorted(os.listdir(tc_dir)):
                if not testcase_id.isnumeric():
                    continue
                new_id = str(1 + int(testcase_id))

            i_meta = FileMetadata.of(path=os.path.join(tc_dir, new_id, "input.txt"))
            o_meta = FileMetadata.of(path=os.path.join(tc_dir, new_id, "output.txt"))
            input_ = TextFile(metadata=i_meta, content="")
            output = TextFile(metadata=o_meta, content="")
            self.text_file_repository.save(input_)
            self.text_file_repository.save(output)
            _open_files(config.general.editor_command, input_, output)
        elif args.edit:
            input_ = self.text_file_repository.find(
                cwd=tc_dir, query=os.path.join(args.edit, "input.txt")
            )
            output = self.text_file_repository.find(
                cwd=tc_dir, query=os.path.join(args.edit, "output.txt")
            )
            _open_files(config.general.editor_command, input_, output)
        else:
            raise FatalError("operation is not specified: --new || -edit $id")
