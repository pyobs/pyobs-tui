from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import RichLog, Input


class pyobsApp(App):
    """A Textual app for pyobs."""

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield RichLog(id="CommandLog", highlight=True, markup=True)
            yield RichLog(id="Log", highlight=True, markup=True)
        yield Input(id="Input")

    @on(Input.Submitted, "#Input")
    def handle_submit(self, event: Input.Submitted) -> None:
        value = event.value.strip()
        self.query_one("#CommandLog", RichLog).write(value)
        event.input.value = ""
