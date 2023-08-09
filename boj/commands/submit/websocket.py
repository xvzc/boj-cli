import json
import asyncio
from rich.console import Console
from websockets import client
from boj.core import util
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)


class Detail:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Message:
    def __init__(self, keep_alive, status, progress, color, error, details):
        self.keep_alive = keep_alive
        self.status = status
        self.progress = progress
        self.error = error
        self.color = color
        self.details = details

    def __repr__(self):
        return (
            "Problem {"
            + str(self.keep_alive)
            + ", "
            + self.color
            + ", "
            + self.status
            + "}"
        )

    @staticmethod
    def unknown_error():
        return Message(
            keep_alive=False,
            error=True,
            progress=cur_progress,
            color="blue",
            status="Unknow Error",
            details=[],
        )


def trace(solution_id):
    try:
        asyncio.run(connect(solution_id))
    except KeyboardInterrupt:
        pass


# Track submit status
async def connect(solution_id):
    progress = Progress(
        SpinnerColumn(style="white", finished_text="•"),
        BarColumn(complete_style="white"),
        TaskProgressColumn(),
        TimeElapsedColumn(),
    )

    with progress:
        task = progress.add_task("", total=100)

        async with client.connect(util.websocket_url()) as websocket:
            await websocket.send(json.dumps(make_subscribe_request(solution_id)))

            cur_progress = 0

            keep_alive = True
            while keep_alive:
                try:
                    data = await asyncio.wait_for(websocket.recv(), timeout=20)
                    data_dict = json.loads(data)
                    message = await parse_message(data_dict)
                    cur_progress = max(message.progress, cur_progress)
                except:
                    message = Message.unknown_error()
                    break

                keep_alive = message.keep_alive
                progress.update(
                    task,
                    completed=cur_progress,
                )

                if not keep_alive:
                    break

            progress.stop()

            console = Console()
            console.print(
                "[white]• [bold " + message.color + "]" + message.status,
            )

            for detail in message.details:
                console.print(
                    "  - " + detail.name + ": " + detail.description,
                    style="white",
                )


def make_subscribe_request(solution_id):
    return {
        "event": "pusher:subscribe",
        "data": {"channel": f"solution-{solution_id}"},
    }


async def parse_message(message: dict):
    if message["event"] == "pusher:connection_established":
        return Message(
            keep_alive=True,
            error=False,
            progress=0,
            color="white",
            status="Wating",
            details=None,
        )

    if message["event"] == "pusher_internal:subscription_succeeded":
        return Message(
            keep_alive=True,
            error=False,
            progress=0,
            color="white",
            status="Wating",
            details=None,
        )

    if message["event"] == "pusher:error":
        raise Exception("Websocket error.")

    if message["event"] != "update":
        raise Exception("Unhandled response")

    data = json.loads(message["data"])
    if "progress" in data:
        progress = int(data["progress"])
    else:
        progress = 0

    if data["result"] <= 2:
        return Message(
            keep_alive=True,
            error=False,
            progress=progress,
            color="green",
            status="Waiting",
            details=[],
        )

    if data["result"] == 3:
        return Message(
            keep_alive=True,
            error=False,
            progress=progress,
            color="white",
            status="Running",
            details=None,
        )

    # Accepted.
    if data["result"] == 4:
        details = [
            Detail(name="Memory", description=str(data["memory"]) + " kb"),
            Detail(name="Time  ", description=str(data["time"]) + " ms"),
        ]

        if "subtask_score" in data:
            details.append(Detail(name="Score ", description=str(data["subtask_score"])))

        return Message(
            keep_alive=False,
            error=False,
            progress=100,
            color="green",
            status="Accepted",
            details=details,
        )

    if data["result"] == 5:
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="red",
            status="Wrong Format",
            details=[],
        )

    if data["result"] == 6:
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="red",
            status="Wrong Answer",
            details=[],
        )

    if data["result"] == 7:
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="red",
            status="Time Limit Exceeded",
            details=[],
        )

    if data["result"] == 8:
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="red",
            status="Memory Limit Exceeded",
            details=[],
        )

    if data["result"] == 9:
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="red",
            status="Output Limit Exceeded",
            details=[],
        )

    if data["result"] == 10:
        details = []
        if "rte_reason" in data:
            details.append(Detail(name="Reason", description=str(data["rte_reason"])))

        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="magenta",
            status="Runtime Error",
            details=details,
        )

    if data["result"] == 11:
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="blue",
            status="Compile Error",
            details=[],
        )

    # Partly accepted
    if data["result"] == 15:
        details = []
        if "subtask_score" in data:
            details.append(Detail(name="Score", description=str(data["subtask_score"])))

        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="yellow",
            status="Partial points",
            details=details,
        )

    # Runtime error invatigation
    if data["result"] == 16:
        return Message(
            keep_alive=True,
            error=False,
            progress=progress,
            color="white",
            status="Looking for the cause of Runtime Error",
            details=[],
        )

    print(data)

    raise Exception("Unhandled response")
