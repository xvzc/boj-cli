import argparse
import os
import pkg_resources  # part of setuptools


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=get_version(),
        help="show version",
    )

    subparsers = parser.add_subparsers(dest="command")  # this line changed
    add_login_parser(subparsers)
    add_submit_parser(subparsers)
    add_open_parser(subparsers)
    add_run_parser(subparsers)
    add_init_parser(subparsers)
    add_random_parser(subparsers)

    return parser


def add_init_parser(subparsers):
    init_parser = subparsers.add_parser(
        "init", help="creates testcases in current directory"
    )
    init_parser.add_argument(
        "problem_id",
        metavar="PROBLEM_ID",
        type=int,
        help="problem id",
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
        "id",
        metavar="PROBLEM_ID",
        type=int,
        help="problem id",
    )


def add_random_parser(subparsers):
    random_parser = subparsers.add_parser(
        "random", help="queries and opens a random problem in browser"
    )
    random_parser.add_argument(
        "--tier",
        default=None,
        help="tier",
    )
    random_parser.add_argument(
        "--tags",
        nargs="*",
        default=None,
        help="tags",
    )


def add_run_parser(subparsers):
    run_parser = subparsers.add_parser("run", help="runs generated testcases")
    run_parser.add_argument(
        "file",
        metavar="FILE",
        type=validate_file,
        help="file path of the source code",
    )
    run_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=None,
        help="show detailed output",
    )
    run_parser.add_argument(
        "-t",
        "--timeout",
        default=None,
        help="timeout for each test",
    )


def add_submit_parser(subparsers):
    # Submit command parser
    submit_parser = subparsers.add_parser(
        "submit",
        help="submits your solution and trace the realtime statement",
    )
    submit_parser.add_argument(
        "file",
        metavar="FILE",
        type=validate_file,
        help="local file path of your source code",
    )
    submit_parser.add_argument(
        "-l",
        "--lang",
        default=None,
        help="language to submit your source code as",
    )
    submit_parser.add_argument(
        "-o",
        "--open",
        default=None,
        type=validate_code_open,
        help="whether to publicly open the submitted code ('open' | 'close' | 'onlyaccepted')",
    )


def get_version():
    try:
        return str(pkg_resources.require("boj-cli")[0]).strip()
    except (Exception,) as e:
        return "0.0.0"


def validate_file(file):
    if os.path.isfile(file):
        return file
    else:
        raise argparse.ArgumentTypeError(f"'{file}' No such file.")


def validate_code_open(value):
    if value not in ['open', 'close', 'onlyaccepted']:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid option.")

    return value
