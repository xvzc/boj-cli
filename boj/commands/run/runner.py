import asyncio
from subprocess import Popen, PIPE
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from boj.core.console import BojConsole

LABEL_LENGTH = 9


def run_compile(command, args):
    file = args.file
    console = BojConsole()
    with console.status("Compiling..") as status:
        try:
            command = command.replace("$file", file)
            process = Popen(
                command,
                stdout=PIPE,
                stderr=PIPE,
                shell=True,
                text=True,
            )

            out, err = process.communicate()
            console.log("-------------------------------")

            if out and args.verbose:
                console.log("[bold white]Compile output:")
                console.log(out)

            if err and args.verbose:
                console.log("[bold white]Compile output:")
                console.log(err)

            if process.returncode != 0:
                status.stop()
                console.print_err("Compile error.")
                exit(1)

        except Exception as e:
            console.log(e)
            console.print_err("Compile error.")


def run_testcases(command, testcase_dict, args):
    testcases = []

    for k in testcase_dict:
        testcases.append(testcase_dict[k])

    progress = Progress(
        SpinnerColumn(style="white", finished_text="•"),
        TextColumn("[progress.description]{task.description}"),
        console=BojConsole()
    )

    with progress:
        num_of_testcases = len(testcases)
        task_ids = []
        for i in range(num_of_testcases):
            task_ids.append(progress.add_task(
                "[white]TEST #" + str(i) + create_label("Running"), total=1)
            )

        futures = []
        for i in range(num_of_testcases):
            futures.append(
                asyncio.ensure_future(
                    run_testcase_async(
                        command=command,
                        testcase=testcases[i],
                        test_index=i + 1,
                        args=args,
                        progress=progress,
                        task_id=task_ids[i],
                    )
                )
            )

        # Run all testcases parallel
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*futures))
        loop.close()


async def run_testcase_async(command, testcase, test_index, args, progress, task_id):
    process = await asyncio.create_subprocess_shell(
        command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        shell=True,
    )

    test_input = testcase["input"].rstrip() if "input" in testcase else ""
    answer = testcase["output"].rstrip() if "output" in testcase else ""

    try:
        out, err = await asyncio.wait_for(process.communicate(input=test_input.encode('utf-8')), timeout=5)

        out = out.decode('utf-8').rstrip()
        err = err.decode('utf-8').rstrip()

        if out and args.verbose:
            progress.console.log(
                "[white]TEST #" + str(test_index)
                + "[bold blue]" + create_label("Run output") + ": "
            )
            progress.console.log(out)

        if err and args.verbose:
            progress.console.log(
                "[white]TEST #" + str(test_index)
                + "[magenta]" + create_label("Runtime error") + ":"
            )
            progress.console.log(err)

        if process.returncode != 0:
            progress.update(task_id,
                            description="[white]TEST #" + str(test_index)
                                        + "[magenta]" + create_label("Error"),
                            completed=1)
            return

        if answer.rstrip() == out:
            progress.update(task_id,
                            description="[white]TEST #" + str(test_index)
                                        + "[green]" + create_label("Passed"),
                            completed=1)
        else:
            progress.update(task_id,
                            description="[white]TEST #" + str(test_index)
                                        + "[red]" + create_label("Failed"),
                            completed=1)
    except asyncio.exceptions.TimeoutError:
        progress.update(task_id,
                        description="[white]TEST #" + str(test_index)
                                    + "[magenta]" + create_label("Timed out"),
                        completed=1)
        return


def create_label(label):
    return " " + label.ljust(9, " ")
