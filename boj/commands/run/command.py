import time
import yaml
from boj.commands.run import runner
import boj.core.util as util
import json

from boj.core.console import BojConsole


def run(args):
    console = BojConsole()

    with console.status("Loading source file...") as status:
        solution = util.read_solution(args.file)
        time.sleep(0.4)

        console.log("Loaded source file.")

        status.update("Loading configuration...")
        time.sleep(0.3)

        config = None
        try:
            f = util.read_file(util.config_file_path(), "r")
            config = json.loads(f)
        except FileNotFoundError:
            status.stop()
            console.print_err("Config file is not found.")
            exit(1)

        if not config or "filetype" not in config or solution.filetype not in config["filetype"]:
            status.stop()
            console.print_err("configuration for " + solution.filetype + " is not found.")
            exit(1)

        filetype_config = config["filetype"][solution.filetype]

        console.log("Loaded configuration.")

    # if filetype_config["compile"]:
    #     status.update("compiling...")
    #     command = filetype_config["compile"]
    #     runner.run_compile(console, command, args.file)

    if not filetype_config["run"]:
        console.print_err("Run command not found.")
        exit(1)

    status.update("Loading testcases...")
    try:
        stream = util.read_file("./testcase.yaml", "r")
        testcases = yaml.safe_load(stream)
        command = filetype_config["run"]
        command = command.replace("$file", args.file)
        status.stop()
        runner.run_test(command, args.file, testcases)
    except FileNotFoundError:
        status.stop()
        console.print_err("Failed to load testcases.")
        exit(1)
    except KeyError:
        status.stop()
        console.print_err("Run command not found.")
        exit(1)
