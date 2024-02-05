import traceback

from boj import args_resolver
from boj.containers import Container
from boj.core import constant
from boj.core.error import BojError
from boj.core.console import BojConsole
from boj.core.fs.util import mkdir


def cli():
    parser = args_resolver.create_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        exit(0)

    console = BojConsole()
    try:
        container = Container()
        dispatcher = container.dispatcher_factory()
        mkdir(constant.boj_cli_path(), True)
        dispatcher.modules[args.command].execute(args)
    except BojError as e:
        SystemExit(e)
        console.log("Error: " + str(e))
        # print(str(e))
        exit(1)
    except BaseException as e:
        console.log(e.args)
        traceback.print_exc()
        exit(1)
