import json

from boj.core.error import WebSocketError


class Detail:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Message:
    def __init__(
        self,
        keep_alive: bool,
        status: str,
        progress: int,
        color: str,
        error: bool,
        details: list[Detail],
    ):
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
    def unknown_error(progress, e: Exception):
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="blue",
            status="Unknown Error",
            details=[Detail(name="Reason", description=str(e))],
        )

    @staticmethod
    def connection_established():
        return Message(
            keep_alive=True,
            error=False,
            progress=0,
            color="white",
            status="Connection Established",
            details=[],
        )

    @staticmethod
    def subscription_succeeded():
        return Message(
            keep_alive=True,
            error=False,
            progress=0,
            color="white",
            status="Subscription Succeeded",
            details=[],
        )

    @staticmethod
    def waiting(progress: int):
        return Message(
            keep_alive=True,
            error=False,
            progress=progress,
            color="green",
            status="Waiting",
            details=[],
        )

    @staticmethod
    def running(progress: int):
        return Message(
            keep_alive=True,
            error=False,
            progress=progress,
            color="white",
            status="Running",
            details=[],
        )

    @staticmethod
    def accepted(details: list[Detail]):
        return Message(
            keep_alive=False,
            error=False,
            progress=100,
            color="green",
            status="Accepted",
            details=details,
        )

    @staticmethod
    def wrong_format(progress: int):
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="red",
            status="Wrong Format",
            details=[],
        )

    @staticmethod
    def wrong_answer(progress: int):
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="red",
            status="Wrong Answer",
            details=[],
        )

    @staticmethod
    def time_limit_exceeded(progress: int):
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="red",
            status="Time Limit Exceeded",
            details=[],
        )

    @staticmethod
    def memory_limit_exceeded(progress: int):
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="red",
            status="Memory Limit Exceeded",
            details=[],
        )

    @staticmethod
    def output_limit_exceeded(progress: int):
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="red",
            status="Output Limit Exceeded",
            details=[],
        )

    @staticmethod
    def runtime_error(progress: int, details: list[Detail]):
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="magenta",
            status="Runtime Error",
            details=details,
        )

    @staticmethod
    def compile_error(progress: int):
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="blue",
            status="Compile Error",
            details=[],
        )

    @staticmethod
    def partial_points(progress: int, details: list[Detail]):
        return Message(
            keep_alive=False,
            error=True,
            progress=progress,
            color="yellow",
            status="Partial points",
            details=details,
        )

    @staticmethod
    def runtime_error_waiting(progress: int):
        return Message(
            keep_alive=True,
            error=False,
            progress=progress,
            color="white",
            status="Looking for the cause of Runtime Error",
            details=[],
        )


async def parse_message(message: dict):
    if message["event"] == "pusher:connection_established":
        return Message.connection_established()

    if message["event"] == "pusher_internal:subscription_succeeded":
        return Message.subscription_succeeded()

    if message["event"] == "pusher:error":
        raise WebSocketError("Websocket error")

    if message["event"] != "update":
        raise WebSocketError("Unknown websocket event")

    data = json.loads(message["data"])
    progress = data["progress"] if "progress" in data else 0

    if data["result"] <= 2:
        return Message.waiting(progress)

    if data["result"] == 3:
        return Message.running(progress)

    # Accepted.
    if data["result"] == 4:
        details = [
            Detail(name="Memory", description=str(data["memory"]) + " kb"),
            Detail(name="Time  ", description=str(data["time"]) + " ms"),
        ]

        if "subtask_score" in data:
            details.append(
                Detail(name="Score ", description=str(data["subtask_score"]))
            )

        return Message.accepted(details)

    if data["result"] == 5:
        return Message.wrong_format(progress)

    if data["result"] == 6:
        return Message.wrong_answer(progress)

    if data["result"] == 7:
        return Message.time_limit_exceeded(progress)

    if data["result"] == 8:
        return Message.memory_limit_exceeded(progress)

    if data["result"] == 9:
        return Message.output_limit_exceeded(progress)

    if data["result"] == 10:
        details = []
        if "rte_reason" in data:
            details.append(Detail(name="Reason", description=str(data["rte_reason"])))

        return Message.runtime_error(progress, details)

    if data["result"] == 11:
        return Message.compile_error(progress)

    # Partial points
    if data["result"] == 15:
        details = []
        if "subtask_score" in data:
            details.append(Detail(name="Score", description=str(data["subtask_score"])))

        return Message.partial_points(progress, details)

    # Runtime error investigation
    if data["result"] == 16:
        return Message.runtime_error_waiting(progress)

    raise WebSocketError("Unknown websocket status")
