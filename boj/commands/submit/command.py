import json
from boj.commands.submit import crawler as crawler, websocket
import boj.core.util as util
from time import sleep
from rich.console import Console


def run(args):
    console = Console()

    with console.status(
        "[bold yellow]Loading source code...",
        spinner_style="white",
    ) as status:
        problem = util.read_problem(args.file)
        sleep(0.4)

        status.update("[bold yellow]Authenticating...")

        credential = util.read_credential()
        online_judge = crawler.query_online_judge_token(util.home_url())
        cookies = {
            "bojautologin": credential["token"],
            "OnlineJudge": online_judge,
        }

        submit_url = util.submit_url(problem.id)
        try:
            global csrf_key
            csrf_key = crawler.query_csrf_key(submit_url, cookies)
        except Exception as e:
            status.stop()
            console.print("[bold red]" + str(e))
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
                default_language = config["default_language"][problem.filetype]
                payload["language"] = util.convert_language_code(default_language)
                console.log("[blue]lang [white]option is not provided.")
            except Exception:
                status.stop()
                console.print(
                    "[white]Default language for the given filetype "
                    + "[bold blue]"
                    + problem.filetype
                    + " [white]is not set"
                )
                console.print(
                    "[white]Please set your default languages for certain filetypes in the config file"
                )
                console.print("[white] - Config path: " + util.config_file_path())
                exit(1)

        status.update("[bold yellow]Submitting source code...")
        solution_id = crawler.send_source_code(submit_url, cookies, payload)

    websocket.trace(solution_id)
