import dataclasses
from typing import Dict

from dependency_injector import containers, providers

from boj.commands.case.command import CaseCommand
from boj.commands.clean import CleanCommand
from boj.commands.init import InitCommand
from boj.commands.login import LoginCommand
from boj.commands.open import OpenCommand
from boj.commands.random import RandomCommand
from boj.commands.run import RunCommand
from boj.commands.submit import SubmitCommand
from boj.core.fs.file_io import GeneralFileIO
from boj.core.fs.repository import TextFileRepository
from boj.core.fs.file_search_strategy import UpwardSearchStrategy, StaticSearchStrategy
from boj.commands.add import AddCommand
from boj.core.command import Command
from boj.core.console import BojConsole
from boj.core.fs.serializer import TextFileSerializer
from boj.data.boj_info import BojInfoSerializer, BojInfoRepository
from boj.data.config import ConfigFileSerializer, ConfigRepository
from boj.data.credential import CredentialRepository, CredentialSerializer
from boj.web.boj_problem_page import TitleParser, TestcaseParser
from boj.web.boj_status_page import SolutionIdParser
from boj.web.boj_submit_page import CsrfKeyParser


@dataclasses.dataclass
class Module:
    name: str


@dataclasses.dataclass
class Dispatcher:
    modules: Dict[str, Command]


class Container(containers.DeclarativeContainer):
    console = providers.Singleton(BojConsole)
    config_repository = providers.Factory(
        ConfigRepository,
        serializer=ConfigFileSerializer(),
        file_io=GeneralFileIO(),
        search_strategy=UpwardSearchStrategy(),
    )
    credential_repository = providers.Factory(
        CredentialRepository,
        serializer=CredentialSerializer(),
        file_io=GeneralFileIO(),
        search_strategy=StaticSearchStrategy(),
    )
    boj_info_repository = providers.Factory(
        BojInfoRepository,
        serializer=BojInfoSerializer(),
        file_io=GeneralFileIO(),
        search_strategy=StaticSearchStrategy(),
    )
    text_file_repository = providers.Factory(
        TextFileRepository,
        file_io=GeneralFileIO(),
        serializer=TextFileSerializer(),
        search_strategy=StaticSearchStrategy(),
    )

    dispatcher_factory = providers.Factory(
        Dispatcher,
        modules=providers.Dict(
            init=providers.Factory(
                InitCommand,
                console=console,
                config_repository=config_repository,
            ),
            add=providers.Factory(
                AddCommand,
                console=console,
                config_repository=config_repository,
                boj_info_repository=boj_info_repository,
                text_file_repository=text_file_repository,
                title_parser=TitleParser(),
                testcase_parser=TestcaseParser(),
            ),
            login=providers.Factory(
                LoginCommand,
                console=console,
                credential_repository=credential_repository,
                config_repository=config_repository,
            ),
            clean=providers.Factory(
                CleanCommand,
                console=console,
                config_repository=config_repository,
                boj_info_repository=boj_info_repository,
                text_file_repository=text_file_repository,
            ),
            run=providers.Factory(
                RunCommand,
                console=console,
                config_repository=config_repository,
                boj_info_repository=boj_info_repository,
                text_file_repository=text_file_repository,
            ),
            random=providers.Factory(
                RandomCommand,
                console=console,
                credential_repository=credential_repository,
            ),
            submit=providers.Factory(
                SubmitCommand,
                console=console,
                config_repository=config_repository,
                boj_info_repository=boj_info_repository,
                credential_repository=credential_repository,
                text_file_repository=text_file_repository,
                csrf_key_parser=CsrfKeyParser(),
                solution_id_parser=SolutionIdParser(),
            ),
            open=providers.Factory(
                OpenCommand,
                console=console,
                boj_info_repository=boj_info_repository
            ),
            case=providers.Factory(
                CaseCommand,
                console=console,
                boj_info_repository=boj_info_repository,
                config_repository=config_repository,
                text_file_repository=text_file_repository
            )
        ),
    )
