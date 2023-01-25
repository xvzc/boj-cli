from boj.commands.submit import crawler as crawler, websocket
import boj.core.util as util


def run(args):
    # if not args.path:
    #     raise Exception("No soruce file path provided.")

    print(args.path)

    return

    util.print_white("\rAuthenticating.    ")

    credential = util.read_credential()
    online_judge = crawler.query_online_judge_token(util.home_url())
    cookies = {
        "bojautologin": credential["token"],
        "OnlineJudge": online_judge,
    }

    util.print_white("\rAuthenticating..   ")

    problem = util.read_problem(args.file)


    submit_url = util.submit_url(problem.id)

    csrf_key = crawler.query_csrf_key(submit_url, cookies)

    util.print_white("\rAuthenticating...  ")

    # Set payload for the submit request
    payload = {
        "csrf_key": csrf_key,
        "problem_id": problem.id,
        "language": util.convert_language_code(problem.filetype),
        "code_open": "open",
        "source": problem.source,
    }

    solution_id = crawler.send_source_code(submit_url, cookies, payload)


    websocket.trace(solution_id)
