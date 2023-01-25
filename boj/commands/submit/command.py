from boj.commands.submit import crawler as crawler, websocket
import boj.core.util as util
from time import sleep
from rich.console import Console


def run(args):
    console = Console()

    with console.status("[bold green]Loading source code...") as status:
        problem = util.read_problem(args.file)
        sleep(0.6)

    with console.status("[bold green]Authenticating...") as status:
        credential = util.read_credential()
        online_judge = crawler.query_online_judge_token(util.home_url())
        cookies = {
            "bojautologin": credential["token"],
            "OnlineJudge": online_judge,
        }

        submit_url = util.submit_url(problem.id)

        csrf_key = crawler.query_csrf_key(submit_url, cookies)

    # Set payload for the submit request
    payload = {
        "csrf_key": csrf_key,
        "problem_id": problem.id,
        "language": util.convert_language_code(problem.filetype),
        "code_open": "open",
        "source": problem.source,
    }

    with console.status("[bold green]Submitting source code...") as status:
        solution_id = crawler.send_source_code(submit_url, cookies, payload)


    websocket.trace(solution_id)
