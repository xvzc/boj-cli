import os.path
from pathlib import Path

from boj.core.error import ParsingConfigError, ResourceNotFoundError
from boj.core import util
from boj.core.error import IllegalStatementError


class FiletypeConfig:
    def __init__(
        self,
        language: str,
        filename: str,
        source_dir: str,
        compile_: str,
        run: str,
        after: str,
        manifest_files: list[str],
    ):
        self.__language = language
        self.__filename = filename
        self.__source_dir = source_dir
        self.__compile = compile_
        self.__run = run
        self.__after = after
        self.__manifest_files = manifest_files

    @property
    def language(self) -> str:
        return self.__language

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def source_dir(self) -> str:
        return self.__source_dir

    @property
    def compile(self) -> str:
        return self.__compile

    @property
    def run(self) -> str:
        return self.__run

    @property
    def after(self) -> str:
        return self.__after

    @property
    def manifest_files(self) -> list[str]:
        return self.__manifest_files


class WorkspaceConfig:
    def __init__(
        self, root_dir: str, ongoing_dir: str, archive_dir: str, template_dir: str
    ):
        self.__root_dir = os.path.expanduser(root_dir)
        self.__ongoing_dir = os.path.expanduser(ongoing_dir)
        self.__template_dir = template_dir
        self.__archive_dir = archive_dir

    @property
    def root_dir(self) -> str:
        return self.__root_dir

    @property
    def ongoing_dir(self) -> str:
        return self.__ongoing_dir

    @property
    def template_dir(self) -> str:
        return self.__template_dir

    @property
    def archive_dir(self) -> str:
        return self.__archive_dir


class Config:
    __workspace: WorkspaceConfig
    __filetype: dict[str, FiletypeConfig]

    def __init__(self, workspace_config, filetype_config):
        self.__workspace = workspace_config
        self.__filetype = filetype_config

    @property
    def workspace(self) -> WorkspaceConfig:
        return self.__workspace

    @property
    def filetype(self) -> dict[str, FiletypeConfig]:
        return self.__filetype

    def of_filetype(self, ft) -> FiletypeConfig:
        if ft not in self.__filetype:
            raise ParsingConfigError(
                f"filetype config for '{ft}' is not defined in 'config.yaml'"
            )

        filetype_config = self.__filetype[ft]
        if not filetype_config.language:
            raise ParsingConfigError(
                f"'language' option for filetype '{ft}' is not found."
            )

        if not filetype_config.run:
            raise ParsingConfigError(f"'run' option for filetype '{ft}' is not found.")

        return filetype_config

    def get_source_dir(self, problem_id: str, filetype: str):
        filetype_config = self.of_filetype(filetype)
        return os.path.join(
            self.__workspace.ongoing_dir, str(problem_id), filetype_config.source_dir
        )

    @classmethod
    def load(
        cls,
        suffix: str = os.path.join(".boj", "config.yaml"),
        cwd=os.path.expanduser(os.getcwd()),
    ):
        try:
            config_file_path = util.search_file_upward(str(suffix), cwd=cwd)
        except ResourceNotFoundError:
            raise IllegalStatementError(
                "This is not a BOJ directory (or any of the parent directories)"
            )

        try:
            f = util.read_yaml(config_file_path)
        except (Exception,):
            raise IllegalStatementError("Error while reading 'config.yaml'")

        if f is None:
            f = {}

        if "workspace" not in f:
            f["workspace"] = {}

        if "filetype" not in f:
            f["filetype"] = {}

        # Load workspace config
        workspace_root = str(Path(config_file_path.replace(suffix, "")))
        workspace_config = WorkspaceConfig(
            root_dir=workspace_root,
            ongoing_dir=os.path.join(
                workspace_root, f["workspace"].get("ongoing_dir", "")
            ),
            archive_dir=os.path.join(
                workspace_root, f["workspace"].get("archive_dir", "archives")
            ),
            template_dir=str(Path(os.path.join(workspace_root, ".boj", "templates"))),
        )

        if workspace_config.ongoing_dir == workspace_config.archive_dir:
            raise ParsingConfigError(
                "'ongoing_dir' and 'archive_dir' can not be the same"
            )

        # Load filetype config
        filetype_config = {}
        for ft, v in f["filetype"].items():
            filetype_config[ft] = FiletypeConfig(
                language=v.get("language", None),
                filename=v.get("filename", f"main.{ft}"),
                source_dir=v.get("source_dir", ""),
                compile_=v.get("compile", None),
                run=v.get("run", None),
                after=v.get("after", None),
                manifest_files=v.get("manifest_files", []),
            )

        return cls(workspace_config=workspace_config, filetype_config=filetype_config)
