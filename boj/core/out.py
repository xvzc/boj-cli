from typing import Optional

from rich.console import Console, RenderableType
from rich.status import Status
from rich.style import StyleType


class BojConsole(Console):
    pass

    def __init__(self):
        super().__init__(log_time=False, log_path=False)

    def print_err(self, message):
        super().print("Error: " + message)

    def status(
        self,
        status: RenderableType,
        *,
        spinner: str = "dots",
        spinner_style: str = "status.spinner",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
    ) -> "Status":
        status_renderable = BojStatus(
            f"[bold yellow]{status}",
            console=self,
            spinner=spinner,
            spinner_style="white",
            speed=speed,
            refresh_per_second=refresh_per_second,
        )
        return status_renderable


class BojStatus(Status):
    pass

    status_color: str = "[bold yellow]"

    def __init__(
        self,
        status: RenderableType,
        *,
        console: Optional[Console] = None,
        spinner: str = "dots",
        spinner_style: StyleType = "status.spinner",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
    ):
        super().__init__(
            status=status,
            console=console,
            spinner=spinner,
            spinner_style=spinner_style,
            speed=speed,
            refresh_per_second=refresh_per_second,
        )

    def update(
        self,
        status: Optional[RenderableType] = None,
        *,
        spinner: Optional[str] = None,
        spinner_style: Optional[StyleType] = None,
        speed: Optional[float] = None,
    ) -> None:
        super().update(status=f"{self.status_color}{status}")
