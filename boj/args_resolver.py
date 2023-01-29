import argparse
import os


def create_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")  # this line changed

    # Login command parser
    login_parser = subparsers.add_parser(
        "login",
        help="log in to BOJ",
    )
    login_parser.add_argument(
        "-u",
        "--user",
        required=True,
        help="username",
    )
    login_parser.add_argument(
        "-t",
        "--token",
        required=True,
        help="auto login token",
    )

    # Submit command parser
    submit_parser = subparsers.add_parser("submit", help="submit your solution")
    submit_parser.add_argument(
        "file",
        metavar="FILE",
        type=validate_file,
        help="local file path of your source code",
    )
    submit_parser.add_argument(
        "-l",
        "--lang",
        help="language to submit your source code as",
    )

    problem_parser = subparsers.add_parser(
        "problem", help="show markdown-like problem in terminal"
    )
    problem_parser.add_argument(
        "id",
        metavar="PROBLEM_ID",
        type=int,
        help="problem id",
    )

    run_parser = subparsers.add_parser("run", help="run all testcases")
    run_parser.add_argument(
        "file",
        metavar="FILE",
        type=validate_file,
        help="the file path of the source code",
    )
    run_parser.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        help="show detailed output",
    )
    run_parser.add_argument(
        "-t",
        "--timeout",
        default=5,
        help="timeout for each test",
    )

    init_parser = subparsers.add_parser("init", help="create testcases in current directory")
    init_parser.add_argument(
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
