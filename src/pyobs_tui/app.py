from os.path import basename
from typing import Any

from astropy.time import Time
from pyobs.events import Event, LogEvent
from pyobs.modules import Module
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalGroup
from textual.widget import Widget
from textual.widgets import RichLog, Input, TabbedContent, TabPane, Label


class Shell(VerticalGroup):  # type: ignore
    def compose(self) -> ComposeResult:
        yield RichLog(highlight=True, markup=True)
        yield Input()

    # def on_mount(self) -> None:
    #    self.query_one(Input).focus()

    @on(Input.Submitted)
    def handle_submit(self, event: Input.Submitted) -> None:
        value = event.value.strip()
        self.query_one(RichLog).write(value)
        event.input.value = ""


class Log(VerticalGroup):  # type: ignore
    def compose(self) -> ComposeResult:
        yield RichLog(highlight=True, markup=True)

    def process_log_entry(self, entry: Event, sender: str) -> None:
        """Process a new log entry.

        Args:
            entry: The log event.
            sender: Name of sender.
        """
        if not isinstance(entry, LogEvent):
            return

        # date
        time = Time(entry.time, format="unix")

        # level
        match entry.level:
            case "DEBUG" | "INFO":
                level = f"[green]{entry.level}[/green]"
            case "WARNING":
                level = f"[yellow]{entry.level}[/yellow]"
            case "ERROR":
                level = f"[red]{entry.level}[/red]"
            case _:
                level = entry.level

        # add line
        line = f"[{time.iso.split()[1]}] {sender} {level} {basename(entry.filename)}:{entry.line} {entry.message}"
        self.query_one(RichLog).write(line)


class pyobsApp(App):
    """A Textual app for pyobs."""

    def __init__(self, module: Module, **kwargs: Any):
        App.__init__(self, **kwargs)
        self.module = module

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Log"):
                yield Log()
            with TabPane("Shell"):
                yield Shell()

    async def process_log_entry(self, entry: Event, sender: str) -> bool:
        self.query_one(Log).process_log_entry(entry, sender)
        return True
