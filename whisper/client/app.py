"""
The module contains the client application object.
"""

import signal
import logging
import threading
from typing import Self, NoReturn

from whisper.client.backend import Client
from whisper.client.settings import Setting
from whisper.ui.window import MainWindow
from whisper.ui.theme import Palette
from whisper.client.handlers import Handlers
from whisper.components.root import Root
from whisper.components.splash_screen import SplashWindow
from whisper.packet.v1 import ExitV1Packet, ExitReason
from whisper.typing import (
    TcpClient as _TcpClient,
    TkPalette as _TkPalette,
)


logger = logging.getLogger(__name__)

class App(Client, MainWindow):
    """Main application (Frontend + Backend).

    Frontend is synchronous and is running on `MainThread` while the backend is
    asynchronous and is running on `BackendThread`.

    Use `mainloop` to run the application.
    """

    def __init__(self, title: str, setting: Setting, conn: _TcpClient):
        """The `conn` object is used to connect with the servers."""
        MainWindow.__init__(self)

        self.setting = setting
        self.splash = SplashWindow(self)
        self.handlers = {version: {
            handler.unique_key(): handler(self) for handler in Handlers[version]
        } for version in Handlers.keys()}

        Client.__init__(self, config=setting.cfg, conn=conn)

        self.root = Root(self)
        self.thread = threading.Thread(target=self.run_backend, name="BackendThread")
        self.title(title)
        self.minsize(200, 200)
        self.configure_app()

    def configure_app(self):
        """Configure the application settings. Use this to setup custom
        configuration."""
        self.on_window_exit(lambda: self.shutdown(ExitReason.SELF_EXIT))
        palette_opts = self.create_palette(self.setting.theme.palette)
        self.set_palette(self.setting.theme.palette.base, **palette_opts)
        self.set_theme(self.setting.theme)
        self.set_font(**self.setting.theme.font)
        self.setup_root()
        self.splash.setup()

    def setup_root(self):
        """Setups the root widget of the window and its children."""
        self.root.setup()
        self.root.pack(fill="both", expand=1)

    @property
    def app(self) -> Self:
        """Refrence to the instance object (or itself)."""
        return self

    def run(self):
        """Starts the application."""
        self.handle_signals()
        self.run_thread()
        self.splash.show_window()
        try:
            self.mainloop()
        except BaseException as ex:
            logger.exception(str(ex))
            self.shutdown(ExitReason.EXCEPTION)
        finally:
            logger.info("mainloop exited")

    def mainloop(self, n: int = 0):
        logger.info("mainloop running")
        return MainWindow.mainloop(self, n)

    def run_backend(self):
        """Backend thread target callback."""
        if self.thread != threading.current_thread():
            logger.warning("application backend is running in another thread")
        if self.run_main(self.main) is None:
            logger.info("eventloop exited")
        else:
            logger.info("eventloop exited due to exception")

    def run_thread(self):
        """Starts the backend thread safely."""
        tname = self.thread.name
        if not self.thread.is_alive():
            self.thread.start()
            logger.info(f"{tname} running")
        else:
            logger.warning(f"{tname} is already running")

    async def main(self):
        """Backend lifecycle."""
        self.open_connection()
        await Client.main(self)
        if reason := self.stop_main_result():
            packet = ExitV1Packet.request(reason)
            await self.write(packet, self.loop)
        self.close_connection()

    def shutdown(self, reason: ExitReason | None = None):
        """Safely closes backend thread.."""
        logger.info("shutting down application")
        if self.thread.is_alive():
            logger.debug("closing backend")
            self.stop_main(reason)
            self.thread.join()
            logger.info(f"{self.thread.name} joined")
        MainWindow.quit(self)

    def handle_signals(self):
        signals = []
        if threading.current_thread() is threading.main_thread():
            for sig in self.signals:
                try:
                    signal.signal(sig, lambda _s, _f: self.shutdown(ExitReason.FORCE_EXIT))
                except Exception:
                    logger.exception(f"failed to attach signal handler: {sig}")
                else:
                    logger.debug(f"attached signal handler: {sig}")
                    signals.append(sig)
        return signals

    def signal_handler(self, sig: int): # type: ignore[override]
        """Handles signal passed to application."""
        logger.info(f"received signal: {sig}")
        self.shutdown(ExitReason.FORCE_EXIT)

    async def handler_coro(self) -> NoReturn:
        """Handles incoming packets from queue and writes outgoing packets to queue."""
        logger.info("handler_coro running")
        while True:
            packet = await self.recvq.get()
            handler = self.handlers[packet.version()][packet.unique_key()]
            handler(packet)

    def initial_tasks(self):
        return super().initial_tasks() | { self.handler_coro }

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
