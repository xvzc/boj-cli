from boj import args_resolver
from boj.commands import login, submit, problem, init, run, random
import traceback

command_dict = {
    "login": login.execute,
    "submit": submit.execute,
    "problem": problem.execute,
    "init": init.execute,
    "run": run.execute,
    "random": random.execute,
}


def entry():
    parser = args_resolver.create_parser()
    try:
        args = parser.parse_args()
        if args.command is None:
            raise NotImplementedError()

        command_dict[args.command](args)
    except NotImplementedError:
        parser.print_help()
    except Exception as e:
        print(e)
        traceback.print_exc()
        exit(1)
