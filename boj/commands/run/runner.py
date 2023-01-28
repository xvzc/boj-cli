from subprocess import Popen, PIPE
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


def run_test(command, testcase_dict):
    testcases = []

    for k in testcase_dict:
        testcases.append(testcase_dict[k])

    run_command(command, testcases)

    #
    # asyncio.run(
    #     run_command_async(
    #         command,
    #         testcases,
    #     )
    # )


def run_command(command, testcases: list):
    progress = Progress(
        SpinnerColumn(style="white", finished_text="•"),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )

    tasks = []
    for t in testcases:
        tasks.append(progress.add_task("Running", total=1))

    with progress:
        for t in testcases:
            process = Popen(
                command,
                shell=True,
                text=True,
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
            )

            test_input = t["input"] if "input" in t else ""
            answer = t["output"] if "output" in t else ""

            out, err = process.communicate(input=test_input)
            task_id = tasks[testcases.index(t)]

            if err:
                progress.console.log("[magenta]Error:")
                progress.console.log(err)
                progress.update(task_id, description="Error  ")

            if out:
                progress.console.log("[magenta]Output:")
                progress.console.log(out)
                if answer.rstrip() == out.rstrip():
                    progress.update(task_id, description="Passed ", completed=1)

            if process.returncode != 0:
                print("hi3")
                progress.update(task_id, description="Error  ", completed=1)

    # if stdout:
    #     print(f"[stdout]\n{stdout.decode()}")
    # if stderr:
    #     print(f"[stderr]\n{stderr.decode()}")
