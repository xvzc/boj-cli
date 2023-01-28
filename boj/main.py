from boj.commands.login import command as login_command
from boj.commands.submit import command as submit_command
from boj.commands.problem import command as problem_command
from boj.commands.init import command as init_command
from boj.commands.run import command as run_command
import argparse, os, traceback

command_dict = {
    "login": login_command.run,
    "submit": submit_command.run,
    "problem": problem_command.run,
    "init": init_command.run,
    "run": run_command.run,
}


def entry():
    parser = init_parser()
    try:
        gogosing(parser)
    except Exception as e:
        print(e)
        # Persona
        traceback.print_exc()
        exit(1)


def gogosing(parser):
    args = parser.parse_args()

    if args.command is None or args.command not in command_dict:
        parser.print_help()
        return

    command_dict[args.command](args)


def init_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")  # this line changed

    # Login command parser
    login_parser = subparsers.add_parser(
        "login",
        help="logs in to BOJ",
    )
    login_parser.add_argument(
        "-u",
        "--user",
        help="username",
    )
    login_parser.add_argument(
        "-t",
        "--token",
        help="login token from the cookies",
    )

    # Submit command parser
    submit_parser = subparsers.add_parser("submit", help="submits your code")
    submit_parser.add_argument(
        "file",
        metavar="FILE",
        type=validate_file,
        help="the file path of the sorce code",
    )
    submit_parser.add_argument(
        "-l",
        "--lang",
        help="the language to submit your source code as",
    )

    problem_parser = subparsers.add_parser(
        "problem", help="shows the problem in terminal"
    )
    problem_parser.add_argument(
        "id",
        metavar="PROBLEM_ID",
        type=int,
        help="the problem id",
    )

    test_parser = subparsers.add_parser("run", help="run testcases")
    test_parser.add_argument(
        "file",
        metavar="FILE",
        type=validate_file,
        help="the file path of the sorce code",
    )

    create_parser = subparsers.add_parser("init", help="init testcases")
    create_parser.add_argument(
        "problem_id",
        metavar="PROBLEM_ID",
        type=int,
        help="problem id",
    )

    return parser


def validate_file(file):
    if os.path.isfile(file):
        return file
    else:
        raise argparse.ArgumentTypeError(f"'{file}' No such file.")
