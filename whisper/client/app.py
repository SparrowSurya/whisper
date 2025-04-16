"""
The module contains the client application object.
"""

import asyncio
import threading
from typing import Self

from whisper.client.backend import Client
from whisper.client.settings import Setting
from whisper.ui.window import MainWindow
from whisper.ui.theme import Palette
from whisper.layouts.root import Root
from whisper.logger import Logger
from whisper.typing import (
    TcpClient as _TcpClient,
    TkPalette as _TkPalette,
)


class App(Client, MainWindow):
    """Main application (Frontend + Backend).

    Frontend is synchronous and is running on `MainThread` while the backend is
    asynchronous and is running on `BackendThread`.

    Use `mainloop` to run the application.
    """

    def __init__(self, title: str, logger: Logger, setting: Setting, conn: _TcpClient):
        """The `conn` object is used to connect with the servers."""
        MainWindow.__init__(self)
        self.setting = setting
        Client.__init__(self, logger=logger, config=setting.cfg, conn=conn)
        self.thread = threading.Thread(target=self._run_backend, name="BackendThread")
        self.title(title)
        self.minsize(200, 200)
        self.configure_app()

    def configure_app(self):
        """Configure the application settings. Use this to setup custom
        configuration."""
        self.on_window_exit(self.shutdown)
        self.setup_root()

        palette_opts = self.create_palette(self.setting.theme.palette)
        self.set_palette(**palette_opts)

    def setup_root(self):
        """Setups the root widget of the window and its children."""
        self.root = Root(self)
        self.root.pack(fill="both", expand="true")

    @property
    def app(self) -> Self:
        """Refrence to the instance object (or itself)."""
        return self

    def mainloop(self, n: int = 0):
        """Starts the application."""
        try:
            self.logger.info("running mainloop")
            MainWindow.mainloop(self, n)
        except BaseException as ex:
            self.logger.exception(str(ex))
            self.shutdown()

    def _run_backend(self):
        """Starts the backend. This should be running inside `App.thread`."""
        try:
            asyncio.run(self.main()) # TODO - error handler
        except BaseException as ex:
            self.logger.exception(str(ex))
            self.shutdown()

    def run(self):
        """Starts the backend thread."""
        tname = self.thread.name
        if not self.thread.is_alive():
            self.thread.start()
            self.logger.info(f"thread {tname} started")
        else:
            self.logger.warning(f"thread {tname} is already running")

    async def main(self):
        """Backend lifecycle."""
        self.open_connection()
        await self.execute()
        self.close_connection()

    def shutdown(self):
        """Safely closes backend thread.."""
        if self.thread.is_alive():
            Client.shutdown(self)
            self.thread.join()
            self.logger.info(f"thread {self.thread.name} joined")
        MainWindow.quit(self)
        self.logger.info("mainloop exited")

    def init_connection(self): # TODO
        """Opens a dialogue box for required details."""

    def create_palette(self, palette: Palette) -> _TkPalette:
        """Create palette options from color palette."""
        return {
            "activeBackground": palette.surface0,
            "activeForeground": palette.blue,
            "background": palette.base,
            "disabledBackground": palette.surface0,
            "disabledForeground": palette.overlay0,
            "foreground": palette.text,
            "highlightBackground": palette.surface2,
            "highlightColor": palette.lavender,
            "insertBackground": palette.pink,
            "selectBackground": palette.blue,
            "selectColor": palette.base,
            "selectForeground": palette.base,
            "troughColor": palette.surface0,
        }
