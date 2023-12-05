import traceback

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
from boj.core.error import BojError
from boj.core.out import BojConsole


class CommandFactory:
    @classmethod
    def get(cls, command: str) -> Command:
        return {
            "init": InitCommand(),
            "add": AddCommand(),
            "login": LoginCommand(),
            "open": OpenCommand(),
            "random": RandomCommand(),
            "run": RunCommand(),
            "submit": SubmitCommand(),
            "clean": CleanCommand(),
        }[command]


def cli():
    parser = args_resolver.create_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        exit(0)

    console = BojConsole()
    try:
        util.create_temp_dir()
        CommandFactory.get(args.command).execute(args)
    except BojError as e:
        SystemExit(e)
        console.log("Error: " + str(e))
        # print(str(e))
        exit(1)
    except BaseException as e:
        console.log(e.args)
        traceback.print_exc()
        exit(1)
