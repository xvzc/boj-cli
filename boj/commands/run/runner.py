import asyncio
import time
from random import uniform
from subprocess import Popen, PIPE
from rich.progress import Progress, SpinnerColumn, TextColumn

from boj.core.data import RunnerConfig, Testcase
from boj.core.error import RunCodeError
from boj.core.out import BojConsole


def _create_status_label(color, label):
    return "[" + color + "]" + label.ljust(9, " ")


def _create_testcase_label(index):
    return ("[cyan]#" + str(index)).ljust(10, " ")


def _create_output_label(index, color):
    return ("[" + color + "]" + "OUTPUT [cyan]#" + str(index)).ljust(26, " ")


class Output:
    testcase_id: int
    text: str
    color: str
    ok: bool

    def __init__(self, testcase_id, text, color, ok):
        self.testcase_id = testcase_id
        self.text = text
        self.color = color
        self.ok = ok


class CodeRunner:
    file_path: str
    runner_config: RunnerConfig
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
                    raise RunCodeError('Compile error')

            except Exception as e:
                status.stop()
                raise RunCodeError('Compile error')

    def run_testcases(self):
        progress = Progress(
            SpinnerColumn(style="white", finished_text="•"),
            TextColumn("[progress.description]{task.description}"),
            console=BojConsole()
        )

        with progress:
            testcase_ids = range(1, 1 + len(self.testcases))
            task_ids = []
            for testcase_id in testcase_ids:
                task_ids.append(progress.add_task(
                    _create_testcase_label(testcase_id) + _create_status_label("yellow", "Running"), total=1)
                )

            futures = []
            outputs: list[Output] = []
            for testcase_id, testcase, task_id in zip(testcase_ids, self.testcases, task_ids):
                futures.append(
                    asyncio.ensure_future(
                        self.run_testcase_async(
                            testcase=testcase,
                            testcase_id=testcase_id,
                            progress=progress,
                            task_id=task_id,
                            outputs=outputs,
                        )
                    )
                )

            # Run all testcases parallel
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.gather(*futures))
            loop.close()

            outputs.sort(key=lambda x: x.testcase_id)
            for output in outputs:
                if output.ok:
                    label = _create_output_label(output.testcase_id, output.color)
                else:
                    label = _create_output_label(output.testcase_id, output.color)

                progress.console.log(label)
                progress.console.log(output.text, "\n")

    async def run_testcase_async(
            self, testcase_id: int,
            testcase: Testcase,
            progress,
            task_id,
            outputs: list[Output],
    ):
        process = await asyncio.create_subprocess_shell(
            self.runner_config.run,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=True,
        )

        test_input = testcase.data_in.rstrip()
        answer = testcase.data_out.rstrip()

        try:
            output, error = await asyncio.wait_for(process.communicate(input=test_input.encode('utf-8')), timeout=10)

            output = output.decode('utf-8').rstrip()
            error = error.decode('utf-8').rstrip()

            await asyncio.sleep(uniform(0.2, 1.5))

            if process.returncode != 0:
                color = "bold magenta"
                outputs.append(Output(testcase_id=testcase_id, text=error, color=color, ok=False))
                progress.update(
                    task_id=task_id,
                    description=_create_testcase_label(testcase_id) + _create_status_label(color, "ERROR"),
                    completed=1
                )
                return

            if answer.rstrip() == output:
                color = "bold green"
                outputs.append(Output(testcase_id=testcase_id, text=output, color=color, ok=True))
                progress.update(
                    task_id=task_id,
                    description=_create_testcase_label(testcase_id) + _create_status_label(color, "PASSED"),
                    completed=1
                )
            else:
                color = "bold red"
                outputs.append(Output(testcase_id=testcase_id, text=output, color=color, ok=False))
                progress.update(
                    task_id=task_id,
                    description=_create_testcase_label(testcase_id) + _create_status_label(color, "FAILED"),
                    completed=1
                )

        except asyncio.exceptions.TimeoutError:
            progress.update(
                task_id=task_id,
                description=_create_testcase_label(testcase_id) + _create_status_label("magenta", "Timed out"),
                completed=1
            )
            return
