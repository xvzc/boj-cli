import json, time
from boj.commands.submit import crawler as crawler, websocket
import boj.core.util as util
from boj.core.console import BojConsole


def execute(args):
    console = BojConsole()

    with console.status("Loading source file...") as status:
        problem = util.read_solution(args.file)

        status.update("Authenticating...")
        credential = util.read_credential()
        if not credential:
            status.stop()
            console.print_err("Login required.")

        online_judge = crawler.query_online_judge_token(util.home_url())
        cookies = {
            "bojautologin": credential["token"],
            "OnlineJudge": online_judge,
        }

        submit_url = util.submit_url(problem.id)
        csrf_key = crawler.query_csrf_key(submit_url, cookies)
        if not csrf_key:
            status.stop()
            console.print_err("Authentication failed.")
            exit(1)

        # Set payload for the submit request
        payload = {
            "csrf_key": csrf_key,
            "problem_id": problem.id,
            "language": 0,
            "code_open": "open",
            "source": problem.source,
        }

        if args.lang:
            payload["language"] = util.convert_language_code(args.lang)
        else:
            try:
                f = util.read_file(util.config_file_path(), "r")

                config = json.loads(f)
                filetype_config = config["filetype"][problem.filetype]
                default_language = filetype_config["default_language"]

                payload["language"] = util.convert_language_code(default_language)

                console.log("Default language option is not provided, continuing with your local config.")
                time.sleep(0.7)
            except:
                status.stop()

                console.print_err("Default language for the filetype " + problem.filetype + " is not set.")
                console.print_err("Please set your config for this filetype.")
                console.print_err(" - Config file path: " + util.config_file_path())
                exit(1)

        status.update("Submitting source code...")
        solution_id = crawler.send_source_code(submit_url, cookies, payload)

        console.log("Submission succeeded.")

    websocket.trace(solution_id)
