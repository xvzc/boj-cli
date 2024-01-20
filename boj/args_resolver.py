import argparse
import os
import boj


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=get_version(),
        help="show version",
    )

    subparsers = parser.add_subparsers(dest="command")
    add_init_parser(subparsers)
    add_add_parser(subparsers)
    add_login_parser(subparsers)
    add_open_parser(subparsers)
    add_random_parser(subparsers)
    add_run_parser(subparsers)
    add_submit_parser(subparsers)
    add_clean_parser(subparsers)

    return parser


def add_init_parser(subparsers):
    init_parser = subparsers.add_parser(
        "init", help="initializes BOJ directory"
    )


def add_add_parser(subparsers):
    add_parser = subparsers.add_parser(
        "add", help="sets up an environment of the given problem id"
    )
    add_parser.add_argument(
        "problem_id",
        metavar="PROBLEM_ID",
        type=int,
        help="problem id",
    )
    add_parser.add_argument(
        "-f",
        "--filetype",
        metavar="FILETYPE",
        required=True,
        help="select the filetype to set up the environment with",
    )


def add_login_parser(subparsers):
    subparsers.add_parser(
        "login",
        help="logs in to BOJ",
    )


def add_open_parser(subparsers):
    problem_parser = subparsers.add_parser(
        "open", help="opens a problem of given id in browser"
    )
    problem_parser.add_argument(
        "problem_id",
        metavar="PROBLEM_ID",
        default=None,
        nargs='?',
        type=int,
        help="problem id",
    )


def add_random_parser(subparsers):
    random_parser = subparsers.add_parser(
        "random", help="queries and opens a random problem in browser"
    )
    random_parser.add_argument(
        "-t",
        "--tags",
        nargs="*",
        default=[],
        help="tags",
    )
    random_parser.add_argument(
        "-i",
        "--tier",
        default=None,
        help="tier",
    )


def add_run_parser(subparsers):
    run_parser = subparsers.add_parser("run", help="runs generated testcases")
    run_parser.add_argument(
        "problem_id",
        metavar="PROBLEM_ID",
        default=None,
        nargs='?',
        help="problem id",
    )
    run_parser.add_argument(
        "-t",
        "--timeout",
        default=15,
        type=int,
        help="timeout for each test",
    )


def add_submit_parser(subparsers):
    # Submit command parser
    submit_parser = subparsers.add_parser(
        "submit",
        help="submits your solution and trace the realtime statement",
    )
    submit_parser.add_argument(
        "problem_id",
        metavar="PROBLEM_ID",
        default=None,
        nargs='?',
        help="problem id",
    )
    submit_parser.add_argument(
        "-o",
        "--open",
        default="onlyaccepted",
        type=validate_code_open,
        help="whether to publicly open the submitted code ('open' | 'close' | 'onlyaccepted')",
    )
    submit_parser.add_argument(
        "-t",
        "--timeout",
        default=15,
        type=int,
        help="timeout for websocket",
    )


def add_clean_parser(subparsers):
    submit_parser = subparsers.add_parser(
        "clean",
        help="archives accepted source files",
    )
    submit_parser.add_argument(
        "-o",
        "--origin",
        action="store_true",
        default=False,
        help="use the original filename and overwrite the archived file if it is duplicated",
    )


def get_version():
    return f"boj-cli {boj.__version__}"


def validate_code_open(value):
    if value not in ["open", "close", "onlyaccepted", None]:
        raise ValueError(f"'{value}' is not a valid option.")

    return value
