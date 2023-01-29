import time
from boj.commands.run import runner
import boj.core.util as util

from boj.core.console import BojConsole


def execute(args):
    console = BojConsole()

    with console.status("Loading source file...") as status:
        solution = util.read_solution(args.file)
        time.sleep(0.4)

        console.log("Loaded source file.")

        status.update("Loading configuration...")
        time.sleep(0.3)

        config = util.read_config()
        if not config:
            status.stop()
            console.print_err("Config file is not found.")
            exit(1)

        if "filetype" not in config or solution.filetype not in config["filetype"]:
            status.stop()
            console.print_err("configuration for " + solution.filetype + " is not found.")
            exit(1)

        filetype_config = config["filetype"][solution.filetype]
        if "run" not in filetype_config:
            console.print_err("Run command not found.")
            exit(1)

        console.log("Loaded configuration.")

    if "compile" in filetype_config:
        command = filetype_config["compile"].replace("$file", args.file)
        runner.run_compile(command, args)

    testcases = util.read_testcase()
    if not testcases:
        console.print_err("Failed to load testcases.")
        exit(1)

    command = filetype_config["run"].replace("$file", args.file)
    if not command:
        console.print_err("Run command not found.")
        exit(1)

    runner.run_testcases(command, testcases, args)
