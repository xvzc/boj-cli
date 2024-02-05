import os.path
from pathlib import Path
from typing import Type, Self, Dict, Optional, Union

import yaml

from boj.core.fs.repository import ReadOnlyRepository, T
from boj.core.fs.serializer import Serializer
from boj.core.fs.file_object import FileMetadata, FileObject
from boj.core.error import (
    ParsingConfigError,
    IllegalStatementError,
)


class GeneralConfig:
    def __init__(
        self,
        default_filetype: Optional[str],
        editor_command: Optional[str],
        selenium_browser: Optional[str],
    ):
        self.__default_filetype = default_filetype
        self.__editor_command = editor_command
        self.__selenium_browser = selenium_browser

    @property
    def editor_command(self):
        return self.__editor_command

    @property
    def default_filetype(self):
        return self.__default_filetype

    @property
    def selenium_browser(self):
        return self.__selenium_browser

    @classmethod
    def of(cls, data: dict):
        general = data.get("general", {})
        return cls(
            default_filetype=general.get("default_filetype", None),
            editor_command=general.get("editor_command", None),
            selenium_browser=general.get("selenium_browser", None),
        )


class FiletypeConfig:
    def __init__(
        self,
        workspace_root: str,
        ongoing_dir: str,
        filetype: str,
        language: str,
        filename: str,
        source_dir: str,
        compile_: str,
        run: str,
        after: str,
        source_templates: list[str],
        root_templates: list[str],
    ):
        self.__workspace_root = workspace_root
        self.__ongoing_dir = ongoing_dir
        self.__filetype = filetype
        self.__language = language
        self.__filename = filename
        self.__source_dir = source_dir
        self.__compile = compile_
        self.__run = run
        self.__after = after
        self.__source_templates = source_templates
        self.__root_templates = root_templates

    @property
    def filetype(self) -> str:
        return self.__filetype

    @property
    def language(self) -> str:
        return self.__language

    @property
    def filename(self) -> str:
        return self.__filename

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
    def source_templates(self) -> list[str]:
        return self.__source_templates

    @property
    def root_templates(self) -> list[str]:
        return self.__root_templates

    @property
    def source_dir(self) -> str:
        return self.__source_dir

    @classmethod
    def of(
        cls,
        data: any,
        workspace_root: str,
        ongoing_dir: str,
    ) -> Dict[str, Type[Self]]:
        if "filetype" not in data:
            data["filetype"] = {}

        filetype_config = {}
        for ft, v in data["filetype"].items():
            config = FiletypeConfig(
                workspace_root=workspace_root,
                ongoing_dir=ongoing_dir,
                filetype=ft,
                language=v.get("language", None),
                filename=v.get("filename", f"main.{ft}"),
                source_dir=v.get("source_dir", ""),
                compile_=v.get("compile", None),
                run=v.get("run", None),
                after=v.get("after", None),
                source_templates=v.get("source_templates", []),
                root_templates=v.get("root_templates", []),
            )

            if not config.language:
                raise ParsingConfigError(
                    f"missing 'language' option for the filetype {ft}"
                )

            if not config.filename:
                raise ParsingConfigError(
                    f"missing 'filename' option for the filetype {ft}"
                )

            if not config.run:
                raise ParsingConfigError(f"missing 'run' option for the filetype {ft}")

            filetype_config[ft] = config

        return filetype_config


class WorkspaceConfig:
    def __init__(
        self,
        workspace_root: str,
        ongoing_dir: str,
        archive_dir: str,
        template_dir: str,
    ):
        self.__workspace_root = workspace_root
        self.__ongoing_dir = ongoing_dir
        self.__template_dir = template_dir
        self.__archive_dir = archive_dir

    def ongoing_dir(self, abs_: bool):
        if abs_:
            return os.path.join(self.__workspace_root, self.__ongoing_dir)
        else:
            return self.__ongoing_dir

    def problem_dir(self, id_: Union[str, int]) -> str:
        return os.path.join(
            self.__workspace_root,
            self.__ongoing_dir,
            str(id_),
        )

    def archive_dir(self, id_: Union[str, int], abs_: bool = False) -> str:
        if abs_:
            return os.path.join(self.__workspace_root, self.__archive_dir, str(id_))
        else:
            return self.__archive_dir

    def template_dir(self, abs_: bool = False) -> str:
        if abs_:
            return os.path.join(self.__workspace_root, ".boj", self.__template_dir)
        else:
            return self.__template_dir

    def template_file_path(self, filename: str) -> str:
        return os.path.join(self.template_dir(abs_=True), filename)

    @classmethod
    def of(cls, data: any, workspace_root: str) -> Type[Self]:
        if "workspace" not in data:
            data["workspace"] = {}

        workspace = data["workspace"]
        workspace_config = WorkspaceConfig(
            workspace_root=workspace_root,
            ongoing_dir=workspace.get("ongoing_dir", ""),
            archive_dir=workspace.get("archive_dir", "archives"),
            template_dir="templates",
        )

        if workspace_config.ongoing_dir(True) == workspace_config.archive_dir(True):
            raise ParsingConfigError(
                "'workspace.ongoing_dir' and 'workspace.archive_dir' can not be the same"
            )

        return workspace_config


class Config(FileObject):
    __workspace_root: str
    __general: GeneralConfig
    __workspace: WorkspaceConfig
    __filetype: Dict[str, FiletypeConfig]

    def __init__(
        self,
        metadata: FileMetadata,
        workspace_root: str,
        general: GeneralConfig,
        workspace: WorkspaceConfig,
        filetype_config: Dict[str, FiletypeConfig],
    ):
        super().__init__(metadata)
        self.__workspace_root = workspace_root
        self.__general = general
        self.__workspace = workspace
        self.__filetype = filetype_config

    @property
    def workspace_root(self) -> str:
        return self.__workspace_root

    @property
    def general(self) -> GeneralConfig:
        return self.__general

    @property
    def workspace(self) -> WorkspaceConfig:
        return self.__workspace

    def filetype(self, ft) -> FiletypeConfig:
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


class ConfigFileSerializer(Serializer):
    def marshal(self, raw: bytes, metadata: FileMetadata) -> Config:
        data = yaml.safe_load(raw.decode("utf-8")) or {}
        workspace_root = str(Path(metadata.dir).parent.absolute())
        workspace_config = WorkspaceConfig.of(data, workspace_root)
        filetype_config = FiletypeConfig.of(
            data,
            workspace_root,
            workspace_config.ongoing_dir(False),
        )
        general_config = GeneralConfig.of(data)
        return Config(
            metadata=metadata,
            workspace_root=workspace_root,
            general=general_config,
            workspace=workspace_config,
            filetype_config=filetype_config,
        )

    def unmarshal(self, obj: Config) -> bytes:
        raise IllegalStatementError("Config file object should not be unmarshalled")


class ConfigRepository(ReadOnlyRepository[Config]):
    def find(
        self,
        cwd: str = os.getcwd(),
        query: Optional[str] = None,
    ) -> Config:
        path = self._search_strategy.find(
            cwd=cwd,
            query=os.path.join(".boj", "config.yaml"),
        )
        file = self._file_io.read(path)
        return self._serializer.marshal(file, FileMetadata.of(path))
