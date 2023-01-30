import argparse
import os
import pkg_resources  # part of setuptools


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=print_version(),
        help="show version",
    )

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
        "problem", help="view problem in browser"
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

    random_parser = subparsers.add_parser("random", help="view random problem in browser")
    random_parser.add_argument(
        "tier",
        metavar="TIER",
        type=validate_tier,
        help="tier",
    )
    random_parser.add_argument(
        "--easy",
        action='store_true',
        help="5",
    )
    random_parser.add_argument(
        "--normal",
        action='store_true',
        help="3 ~ 4",
    )
    random_parser.add_argument(
        "--hard",
        action='store_true',
        help="1 ~ 2",
    )

    return parser


def print_version():
    version_info = str(pkg_resources.require("boj-cli")[0]).strip()
    return version_info


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
