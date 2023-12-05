import dataclasses
import traceback
from typing import Dict

from dependency_injector import containers, providers
from dependency_injector.wiring import inject

from boj import args_resolver
from boj.commands.add.add_command import AddCommand
from boj.commands.clean import CleanCommand
from boj.commands.init.init_command import InitCommand
from boj.commands.login.login_command import LoginCommand
from boj.commands.open.open_command import OpenCommand
from boj.commands.random.random_command import RandomCommand
from boj.commands.run.run_command import RunCommand
from boj.commands.submit.submit_command import SubmitCommand
from boj.core import util
from boj.core.base import Command
from boj.core.config import Config
from boj.core.error import BojError
from boj.core.out import BojConsole


@dataclasses.dataclass
class Dispatcher:
    commands: Dict[str, Command]


class Container(containers.DeclarativeContainer):
    dispatcher_factory: dict[str, Command] = providers.Factory(
        Dispatcher,
        commands=providers.Dict(
            {
                "init": providers.Factory(InitCommand),
                "add": providers.Factory(AddCommand),
                "login": providers.Factory(LoginCommand),
                "open": providers.Factory(OpenCommand),
                "random": providers.Factory(RandomCommand),
                "run": providers.Factory(RunCommand),
                "submit": providers.Factory(SubmitCommand),
                "clean": providers.Factory(CleanCommand),
            }
        ),
    )


@inject
def cli():
    parser = args_resolver.create_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        exit(0)

    console = BojConsole()
    try:
        util.create_temp_dir()
        container = Container()
        container.dispatcher_factory().commands[args.command].execute(args)
    except BojError as e:
        SystemExit(e)
        console.log("Error: " + str(e))
        # print(str(e))
        exit(1)
    except BaseException as e:
        console.log(e.args)
        traceback.print_exc()
        exit(1)
