import asyncio
import json
from boj.commands.submit import subscription
from boj.commands.submit.subscription import Message

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)
from websockets import client

import boj.core.constant


def subscribe_progress(solution_id):
    try:
        asyncio.run(connect(solution_id))
    except KeyboardInterrupt:
        pass


def _make_subscribe_request(solution_id):
    return {
        "event": "pusher:subscribe",
        "data": {"channel": f"solution-{solution_id}"},
    }


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

        async with client.connect(boj.core.constant.boj_websocket_url()) as websocket:
            await websocket.send(json.dumps(_make_subscribe_request(solution_id)))

            cur_progress = 0

            keep_alive = True
            while keep_alive:
                try:
                    data = await asyncio.wait_for(websocket.recv(), timeout=20)
                    data_dict = json.loads(data)
                    message = await subscription.parse_message(data_dict)
                    cur_progress = max(message.progress, cur_progress)
                except (Exception,) as e:
                    message = Message.unknown_error(cur_progress, e)
                    break

                keep_alive = message.keep_alive
                progress.update(
                    task,
                    completed=cur_progress,
                )

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


