import dataclasses
import traceback
from typing import Dict

from dependency_injector import containers, providers
from dependency_injector.wiring import inject

from boj import args_resolver
from boj.commands.init.init_command import InitCommand
from boj.commands.login.login_command import LoginCommand
from boj.commands.open.open_command import OpenCommand
from boj.commands.random.random_command import RandomCommand
from boj.commands.run.run_command import RunCommand
from boj.commands.submit.submit_command import SubmitCommand
from boj.core import util
from boj.core.base import Command
from boj.core import config
from boj.core.error import BojError


@dataclasses.dataclass
class Dispatcher:
    commands: Dict[str, Command]


class Container(containers.DeclarativeContainer):
    dispatcher_factory: dict[str, Command] = providers.Factory(
        Dispatcher,
        commands=providers.Dict(
            {
                "init": providers.Factory(InitCommand),
                "login": providers.Factory(LoginCommand),
                "open": providers.Factory(OpenCommand),
                "random": providers.Factory(RandomCommand),
                "run": providers.Factory(RunCommand),
                "submit": providers.Factory(SubmitCommand),
            }
        ),
    )


@inject
def cli():
    util.create_boj_dir()
    parser = args_resolver.create_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        exit(0)

    try:
        container = Container()
        container.dispatcher_factory().commands[args.command].execute(args, config.load())
    except BojError as e:
        SystemExit(e)
        print(str(e))
        exit(1)
    except BaseException as e:
        print(e.args)
        traceback.print_exc()
        exit(1)
