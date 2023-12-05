import os.path
from pathlib import Path

from boj.core.error import ParsingConfigError, ResourceNotFoundError
from boj.core import util
from boj.core.error import IllegalStatementError


class FiletypeConfig:
    language: str
    filename: str
    source_dir: str
    compile: str
    run: str
    after: str
    manifest_files: list[str]

    def __init__(
        self,
        language: str,
        filename: str,
        source_dir: str,
        compile_: str,
        run_: str,
        after: str,
        manifest_files: list[str],
    ):
        self.language = language
        self.filename = filename
        self.source_dir = source_dir
        self.compile = compile_
        self.run = run_
        self.after = after
        self.manifest_files = manifest_files

    def get_relative_source_dir(self, problem_id: str):
        return str(Path(os.path.join(relative_dir, self.source_dir)))


class WorkspaceConfig:
    root_dir: str
    problem_dir: str
    archive_dir: str
    template_dir: str

    def __init__(
        self, root_dir: str, problem_dir: str, archive_dir: str, template_dir: str
    ):
        self.root_dir = os.path.expanduser(root_dir)
        self.problem_dir = os.path.expanduser(problem_dir)
        self.template_dir = template_dir
        self.archive_dir = archive_dir


class Config:
    workspace: WorkspaceConfig
    filetype: dict[str, FiletypeConfig]

    def __init__(self, workspace_config, filetype_config):
        self.workspace = workspace_config
        self.filetype = filetype_config
        pass

    def of_filetype(self, ft) -> FiletypeConfig:
        if ft not in self.filetype:
            raise ParsingConfigError(
                f"filetype config for '{ft}' is not defined in 'config.yaml'"
            )

        filetype_config = self.filetype[ft]
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
            self.workspace.problem_dir, str(problem_id), filetype_config.source_dir
        )

    @classmethod
    def load(
        cls,
        suffix: str = os.path.join(".boj", "config.yaml"),
        cwd=os.path.expanduser(os.getcwd()),
    ):
        try:
            config_file_path = util.search_file_in_parent_dirs(str(suffix), cwd=cwd)
        except ResourceNotFoundError:
            raise IllegalStatementError(
                "This is not a BOJ directory (or any of the parent directories)"
            )

        try:
            f = util.read_yaml(config_file_path)
        except (Exception,) as e:
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
            problem_dir=os.path.join(
                workspace_root, f["workspace"].get("problem_dir", "")
            ),
            archive_dir=os.path.join(
                workspace_root, f["workspace"].get("archive_dir", "archives")
            ),
            template_dir=str(Path(os.path.join(workspace_root, ".boj", "templates"))),
        )

        # Load filetype config
        filetype_config = {}
        for ft, v in f["filetype"].items():
            filetype_config[ft] = FiletypeConfig(
                language=v.get("language", None),
                filename=v.get("filename", f"main.{ft}"),
                source_dir=v.get("source_dir", ""),
                compile_=v.get("compile", None),
                run_=v.get("run", None),
                after=v.get("after", None),
                manifest_files=v.get("manifest_files", []),
            )

        return cls(workspace_config=workspace_config, filetype_config=filetype_config)
