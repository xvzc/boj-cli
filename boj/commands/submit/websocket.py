import json, asyncio
from websockets import client
from boj.core import util
from boj.core.exception import WrongAnswerException


def trace(solution_id):
    try:
        asyncio.run(connect(solution_id))
    except KeyboardInterrupt:
        pass


# Track submit status
async def connect(solution_id):
    # Connect to the web socket.
    util.clear_line()
    util.print_white("\rWaiting..")
    async with client.connect(util.websocket_url()) as websocket:
        await websocket.send(json.dumps(make_subscribe_request(solution_id)))

        keep_connection, accepted = True, False
        while keep_connection:
            data = await websocket.recv()
            message = json.loads(data)
            keep_connection, accepted = await handle_message(message)

        if not accepted:
            raise WrongAnswerException()


def make_subscribe_request(solution_id):
    return {
        "event": "pusher:subscribe",
        "data": {"channel": f"solution-{solution_id}"},
    }


cur_progress = 0


async def handle_message(message: dict):
    global cur_progress

    if message["event"] == "pusher:connection_established":
        return True, False

    if message["event"] == "pusher_internal:subscription_succeeded":
        return True, False

    if message["event"] == "pusher:error":
        raise Exception("Websocket error.")

    if message["event"] != "update":
        raise Exception("Unhandled response")

    data = json.loads(message["data"])

    if data["result"] <= 2:
        return True, False

    if data["result"] == 3:
        util.print_white("\rRunning.. " + str(cur_progress).rjust(3, " ") + "%")
        if "progress" in data:
            cur_progress = max(cur_progress, int(data["progress"]))

        return True, False

    # Accepted.
    if data["result"] == 4:
        util.clear_line()
        util.print_green("\rAccepted\n")
        util.print_white(" - Memory:" + str(data["memory"]) + " kb\n")
        util.print_white(" - Time:" + str(data["time"]) + " ms\n")
        return False, True

    if data["result"] == 5:
        util.clear_line()
        util.print_yellow("\rWrong Format")
        return False, False

    if data["result"] == 6:
        util.clear_line()
        util.print_red("\rWrong Answer")
        return False, False

    if data["result"] == 7:
        util.clear_line()
        util.print_red("\rTime Limit Exceeded")
        return False, False

    if data["result"] == 8:
        util.clear_line()
        util.print_yellow("\rMemory Limit Exceeded")
        return False, False

    if data["result"] == 9:
        util.clear_line()
        util.print_yellow("\rOutput Limit Exceeded")
        return False, False

    if data["result"] == 10:
        util.clear_line()
        util.print_magenta("\rRuntime Error\n")
        if "rte_reason" in data:
            util.print_white("Reason: " + str(data["rte_reason"]))
        return False, False

    if data["result"] == 11:
        util.clear_line()
        util.print_magenta("\rCompile Error")
        return False, False

    # Partly accepted
    if data["result"] == 15:
        util.clear_line()
        if "subtask_score" in data:
            util.print_yellow("\rScore: " + str(data["subtask_score"]))
        return False, False

    # Partly accepted
    if data["result"] == 16:
        util.clear_line()
        util.print_yellow("\rLooking for the cause of runtime error.")
        return True, False

    print(data)

    raise Exception("Unhandled response")
