from boj.commands.login import command as login_command
from boj.commands.submit import command as submit_command
import argparse, os

from boj.core.exception import WrongAnswerException

command_dict = {
    "login": login_command.run,
    "submit": submit_command.run,
}


def entry():
    parser = init_parser()
    try:
        gogosing(parser)
    except WrongAnswerException as e:
        exit(1)
    except Exception as e:
        print(e)
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
    login_parser = subparsers.add_parser("login", help="logs in to BOJ")
    login_parser.add_argument("-u", "--user", help="username")
    login_parser.add_argument("-t", "--token", help="login token from the cookies")

    # Submit command parser
    submit_parser = subparsers.add_parser("submit", help="submits your code")
    submit_parser.add_argument("path", metavar='PATH', type=validate_file, help="the file path of the sorce code")

    return parser

def validate_file(file):
    if os.path.isfile(file):
        return file
    else:
        raise argparse.ArgumentTypeError(f"'{file}' No such file.")


