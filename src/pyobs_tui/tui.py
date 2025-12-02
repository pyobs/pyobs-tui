from typing import Any
from pyobs.modules import Module

from .app import pyobsApp


class TUI(Module):
    __module__ = "pyobs_tui"

    def __init__(self, *args: Any, **kwargs: Any):
        """Inits a new TUI."""

        # init module
        Module.__init__(self, *args, **kwargs)

    async def main(self) -> None:
        """Main loop for application."""
        app = pyobsApp()
        await app.run_async()
