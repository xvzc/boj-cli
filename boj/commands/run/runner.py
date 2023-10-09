import asyncio
from random import uniform
from subprocess import Popen, PIPE

from rich.progress import Progress, SpinnerColumn, TextColumn

from boj.core.data import Testcase
from boj.core.config import FiletypeConfig
from boj.core.error import RunCodeError
from boj.core.out import BojConsole


def _create_status_label(color, label):
    return "[" + color + "]" + label.ljust(9, " ")


def _create_testcase_label(task_id):
    return ("[cyan]#" + str(task_id + 1)).ljust(10, " ")


def _create_output_label(task_id, color):
    return ("[" + color + "]" + "OUTPUT [cyan]#" + str(task_id + 1)).ljust(26, " ")


class Output:
    testcase_id: int
    text: str
    color: str

    def __init__(self, task_id, text, color):
        self.testcase_id = task_id
        self.text = text
        self.color = color


class CodeRunner:
    file_path: str
    runner_config: FiletypeConfig
    testcases: list[Testcase]
    verbose: bool

    def __init__(self, file_path, runner_config, testcases, verbose):
        self.file_path = file_path
        self.runner_config = runner_config
        self.verbose = verbose
        self.testcases = testcases

    def run_compile(self):
        console = BojConsole()

        if not self.runner_config.compile:
            return

        with console.status("Compiling..") as status:
            try:
                command = self.runner_config.compile.replace("$file", self.file_path)
                process = Popen(
                    command,
                    stdout=PIPE,
                    stderr=PIPE,
                    shell=True,
                    text=True,
                )

                output, error = process.communicate()

                if output:
                    console.log(output)

                if error:
                    console.log(error)

                if process.returncode != 0:
                    raise RunCodeError("Compile error")

            except Exception as e:
                status.stop()
                raise RunCodeError("Compile error")

    def run_testcases(self):
        progress = Progress(
            SpinnerColumn(style="white", finished_text="•"),
            TextColumn("[progress.description]{task.description}"),
            console=BojConsole(),
        )

        with progress:
            task_ids = [
                progress.add_task(
                    _create_testcase_label(testcase_id)
                    + _create_status_label("yellow", "Running"),
                    total=1,
                )
                for testcase_id in range(len(self.testcases))
            ]

            futures = [
                asyncio.ensure_future(
                    self._run_testcase_async(
                        task_id=task_id,
                        testcase=testcase,
                        progress=progress,
                    )
                )
                for task_id, testcase in zip(task_ids, self.testcases)
            ]

            # Run all testcases parallel
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.gather(*futures))
            loop.close()

            outputs = sorted(
                [future.result() for future in futures], key=lambda x: x.testcase_id
            )

            if self.verbose:
                for output in outputs:
                    progress.console.log(
                        _create_output_label(output.testcase_id, output.color)
                    )
                    progress.console.log(output.text, end="\n\n")

    async def _run_testcase_async(
        self,
        task_id,
        testcase: Testcase,
        progress,
    ):
        process = await asyncio.create_subprocess_shell(
            self.runner_config.run.replace("$file", self.file_path),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=True,
        )

        test_input = testcase.data_in.rstrip()
        answer = testcase.data_out.rstrip()

        try:
            output, error = await asyncio.wait_for(
                process.communicate(input=test_input.encode("utf-8")), timeout=10
            )

            output = output.decode("utf-8").rstrip()
            error = error.decode("utf-8").rstrip()

            await asyncio.sleep(uniform(0.2, 1.5))

            if process.returncode != 0:
                color = "bold magenta"
                progress.update(
                    task_id=task_id,
                    description=_create_testcase_label(task_id)
                    + _create_status_label(color, "ERROR"),
                    completed=1,
                )
                return Output(task_id=task_id, text=error, color=color)

            if answer.rstrip() == output:
                color = "bold green"
                progress.update(
                    task_id=task_id,
                    description=_create_testcase_label(task_id)
                    + _create_status_label(color, "PASSED"),
                    completed=1,
                )
                return Output(task_id=task_id, text=output, color=color)
            else:
                color = "bold red"
                progress.update(
                    task_id=task_id,
                    description=_create_testcase_label(task_id)
                    + _create_status_label(color, "FAILED"),
                    completed=1,
                )
                return Output(task_id=task_id, text=output, color=color)

        except asyncio.exceptions.TimeoutError:
            progress.update(
                task_id=task_id,
                description=_create_testcase_label(task_id)
                + _create_status_label("magenta", "Timed out"),
                completed=1,
            )
            return
