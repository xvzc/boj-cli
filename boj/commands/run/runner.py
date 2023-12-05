import asyncio
import time
from random import uniform
from subprocess import Popen, PIPE

from rich.progress import Progress, SpinnerColumn, TextColumn

from boj.data.testcase import Testcase, TomlTestcase
from boj.core.config import FiletypeConfig
from boj.core.error import RunCodeError
from boj.core.out import BojConsole
from boj.core import util


def _create_case_label(width, label: str):
    label = label.ljust(width + 1, " ")
    return f"[cyan]CASE #{label}"


def _create_status_label(color, label: str):
    return f"[{color}]{label}"


class Output:
    testcase: Testcase
    task_id: Testcase
    text: str
    color: str

    def __init__(self, testcase, task_id, text, color):
        self.testcase = testcase
        self.task_id = task_id
        self.text = text
        self.color = color


class CodeRunner:
    file_path: str
    language_config: FiletypeConfig
    toml_testcase: TomlTestcase
    timeout: int

    def __init__(self, file_path, ft_config, testcases, timeout):
        self.file_path = file_path
        self.language_config = ft_config
        self.toml_testcase = testcases
        self.timeout = timeout

    def run_compile(self):
        console = BojConsole()

        if not self.language_config.compile:
            return

        with console.status("Compiling..") as status:
            time.sleep(0.3)
            try:
                command = self.language_config.compile.replace("$file", self.file_path)
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
                raise e

    def run_testcases(self):
        progress = Progress(
            SpinnerColumn(style="white", finished_text="•"),
            TextColumn("[progress.description]{task.description}"),
            console=BojConsole(),
        )

        with progress:
            label_width = max([len(testcase.label) for testcase in self.toml_testcase.testcases])
            task_ids = [
                progress.add_task(
                    description=_create_case_label(label_width, testcase.label)
                    + _create_status_label("yellow", "Running.."),
                    total=1,
                )
                for testcase in self.toml_testcase.testcases
            ]

            futures = [
                asyncio.ensure_future(
                    self._run_testcase_async(
                        task_id=task_id,
                        label_width=label_width,
                        testcase=testcase,
                        progress=progress,
                    )
                )
                for task_id, testcase in zip(task_ids, self.toml_testcase.testcases)
            ]

            # Run all testcases parallel
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.gather(*futures))
            loop.close()

            outputs = sorted(
                [future.result() for future in futures], key=lambda x: x.task_id
            )

            progress.console.rule(style="dim white")
            for output in outputs:
                progress.console.log(
                    f"• {_create_case_label(label_width, output.testcase.label)}[{output.color}]OUTPUT"
                )
                progress.console.log("[magenta]Expected:")
                progress.console.log(f"[white]{output.testcase.data_out}", end="")
                progress.console.log("[magenta]Yours:")
                progress.console.log(f"[white]{output.text}", end="")
                progress.console.rule(style="dim white")

    async def _run_testcase_async(
        self,
        label_width,
        task_id,
        testcase: Testcase,
        progress,
    ):
        process = await asyncio.create_subprocess_shell(
            self.language_config.run.replace("$file", self.file_path),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=True,
        )

        answer = testcase.data_out
        test_input = testcase.data_in.encode("utf-8")

        try:
            output, error = await asyncio.wait_for(
                process.communicate(input=test_input), timeout=self.timeout
            )

            output = util.normalize(output.decode("utf-8"))
            error = error.decode("utf-8").rstrip()

            await asyncio.sleep(uniform(0.2, 0.7))

            if process.returncode != 0:
                color = "bold magenta"
                status = "ERROR"
                text = error
            elif answer == output:
                color = "bold green"
                status = "PASSED"
                text = output
            else:
                color = "bold red"
                status = "FAILED"
                text = output

            progress.update(
                task_id=task_id,
                description=_create_case_label(label_width, testcase.label)
                + _create_status_label(color, status),
                completed=1,
            )

            return Output(task_id=task_id, testcase=testcase, text=text, color=color)

        except asyncio.exceptions.TimeoutError:
            color = "magenta"
            status = "TIMED OUT"
            progress.update(
                task_id=task_id,
                description=_create_case_label(label_width, testcase.label)
                + _create_status_label(color, status),
                completed=1,
            )
            return Output(task_id=task_id, testcase=testcase, text="", color=status)

    def post_run(self):
        console = BojConsole()

        if not self.language_config.after:
            return

        try:
            command = self.language_config.after
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
                raise RunCodeError("Error while running 'after' command")

        except Exception as e:
            raise e
