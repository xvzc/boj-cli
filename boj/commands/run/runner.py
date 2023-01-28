import asyncio
from subprocess import Popen, PIPE
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from boj.core.console import BojConsole


def run_compile(command, args):
    file = args.file
    console = BojConsole()
    with console.status("Compiling..") as status:
        try:
            command = command.replace("$file", file)
            process = Popen(
                str.split(command, " "),
                stdout=PIPE,
                stderr=PIPE,
            )

            output, err = process.communicate()
            console.log()

            if output and args.verbose:
                console.log("[bold yellow]Compile output:")
                console.log(err.decode("utf-8"))

            if output and args.verbose:
                console.log("[bold yellow]Compile output:")
                console.log(output.decode("utf-8"))

            if process.returncode != 0:
                status.stop()
                console.print_err("Compile error.")
                exit(1)

        except Exception as e:
            console.log(e)
            console.print_err("Compile error.")


def run_test(command, testcase_dict, args):
    testcases = []

    for k in testcase_dict:
        testcases.append(testcase_dict[k])

    asyncio.run(run_command_async(command, testcases, args))


async def run_command_async(command, testcases: list, args):
    progress = Progress(
        SpinnerColumn(style="white", finished_text="•"),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=BojConsole()
    )

    tasks = []
    for i in range(len(testcases)):
        tasks.append(progress.add_task("[white]TEST" + str(i) + " Running", total=1))

    with progress:
        for i in range(len(testcases)):
            process = await asyncio.create_subprocess_shell(
                command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True,
            )

            test_input = testcases[i]["input"] if "input" in testcases[i] else ""
            answer = testcases[i]["output"] if "output" in testcases[i] else ""

            out, err = await process.communicate(input=test_input.encode('utf-8'))
            task_id = tasks[i]

            if out:
                decoded_err = out.decode('utf-8')
                if args.verbose:
                    progress.console.log("[magenta]Runtime error:")
                    progress.console.log(decoded_err)
                    progress.update(task_id, description="Error  ")

            if out:
                decoded_out = out.decode('utf-8')
                if args.verbose:
                    progress.console.log("[yellow]Run output:")
                    progress.console.log(decoded_out)

                if answer.rstrip() == decoded_out.rstrip():
                    progress.update(task_id, description="[white]TEST" + str(i) + "[green] Passed", completed=1)
                else:
                    progress.update(task_id, description="[white]TEST" + str(i) + "[red] Failed", completed=1)

            if process.returncode != 0:
                progress.update(task_id, description="[white]TEST" + str(i) + "[magenta] Error", completed=1)
