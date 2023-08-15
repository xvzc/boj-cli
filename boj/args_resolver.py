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
    add_problem_parser(subparsers)
    add_run_parser(subparsers)
    add_init_parser(subparsers)
    add_random_parser(subparsers)

    return parser

def add_login_parser(subparsers):
    subparsers.add_parser(
        "login",
        help="log in to BOJ",
    )

def add_submit_parser(subparsers):
    # Submit command parser
    submit_parser = subparsers.add_parser(
        "submit", 
        help="submit your solution",
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
        help="language to submit your source code as",
    )

def add_problem_parser(subparsers):
    problem_parser = subparsers.add_parser(
        "problem", help="view problem in browser"
    )
    problem_parser.add_argument(
        "id",
        metavar="PROBLEM_ID",
        type=int,
        help="problem id",
    )

def add_run_parser(subparsers):
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
        default=10,
        help="timeout for each test",
    )


def add_init_parser(subparsers):
    init_parser = subparsers.add_parser("init", help="create testcases in current directory")
    init_parser.add_argument(
        "problem_id",
        metavar="PROBLEM_ID",
        type=int,
        help="problem id",
    )


def add_random_parser(subparsers):
    random_parser = subparsers.add_parser("random", help="view random problem in browser")
    random_parser.add_argument(
        "--tier",
        help="tier",
    )
    random_parser.add_argument(
        "--tags",
        nargs="*",
        default=[],
        help="tags",
    )


def get_version():
    try:
        return str(pkg_resources.require("boj-cli")[0]).strip()
    except:
        return "0.0.0"


def validate_file(file):
    if os.path.isfile(file):
        return file
    else:
        raise argparse.ArgumentTypeError(f"'{file}' No such file.")


def validate_tier(tier):
    allowed_tier = ["bronze", "silver", "gold", "platinum", "diamond", "ruby"]
    if tier not in allowed_tier:
        raise argparse.ArgumentTypeError(f"available values for tier parameter: {allowed_tier}")

    return tier
