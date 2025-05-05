"""
The module contains the client application object.
"""

import signal
import threading
from typing import Self

from whisper.client.backend import Client
from whisper.client.settings import Setting
from whisper.ui.window import MainWindow
from whisper.ui.theme import Palette
from whisper.components.root import Root
from whisper.components.conn_init_form import ConnInitFormDialog
from whisper.logger import Logger
from whisper.packet.v1 import ExitPacket, ExitReason
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
        self.root = Root(self)
        self.thread = threading.Thread(target=self._run_backend, name="BackendThread")
        self.title(title)
        self.minsize(200, 200)
        self.configure_app()

    def configure_app(self):
        """Configure the application settings. Use this to setup custom
        configuration."""
        self.on_window_exit(lambda: self.shutdown(ExitReason.SELF_EXIT))
        palette_opts = self.create_palette(self.setting.theme.palette)
        self.set_palette(**palette_opts)
        self.set_theme(self.setting.theme)
        self.set_font(**self.setting.theme.font)
        self.setup_root()

    def setup_root(self):
        """Setups the root widget of the window and its children."""
        self.root.setup()
        self.root.pack(fill="both", expand="true")

    @property
    def app(self) -> Self:
        """Refrence to the instance object (or itself)."""
        return self

    def mainloop(self, n: int = 0):
        """Starts the application."""
        signals = self.handle_signals()
        self.logger.info(f"handelling signals: {signals}")
        self.after(1000, self.run)
        self.logger.info("running mainloop")
        try:
            MainWindow.mainloop(self, n)
        except BaseException as ex:
            self.logger.exception(str(ex))
            self.shutdown(ExitReason.EXCEPTION)

    def _run_backend(self):
        """Starts the backend. This should be running inside `App.thread`."""
        exc_info = self.run_main(self.main)
        if exc_info is not None:
            self.logger.exception("eventloop returned with error", exc_info=exc_info)

    def run(self):
        """Starts the backend thread."""
        tname = self.thread.name
        if not self.thread.is_alive():
            self.thread.start()
            self.logger.info(f"{tname} running")
        else:
            self.logger.warning(f"{tname} is already running")

    async def main(self):
        """Backend lifecycle."""
        self.open_connection()
        self.init_connection()
        await Client.main(self)
        if reason := self.stop_main_result():
            await self.write(ExitPacket.request(reason), self.loop)
        self.close_connection()

    def shutdown(self, reason: ExitReason | None = None):
        """Safely closes backend thread.."""
        if self.thread.is_alive():
            self.stop_main(reason)
            self.thread.join()
            self.logger.info(f"{self.thread.name} joined")
        MainWindow.quit(self)
        self.logger.info("mainloop exited")

    def handle_signals(self):
        signals = []
        for sig in self.signals:
            try:
                signal.signal(sig, lambda _s, _f: self.shutdown(ExitReason.FORCE_EXIT))
            except ValueError:
                pass
            else:
                signals.append(sig)
        return signals

    def signal_handler(self, sig: int): # type: ignore[override]
        """Handles signal passed to application."""
        self.logger.info(f"received signal: {sig!r}")
        self.shutdown(ExitReason.FORCE_EXIT)

    def init_connection(self): # TODO
        """Opens a dialogue box for required details."""

        def callback(**kwargs):
            nonlocal self, dialog
            Client.init_connection(self, **kwargs)
            dialog.close()

        dialog = ConnInitFormDialog(self, callback)
        dialog.setup()

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
