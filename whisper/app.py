"""
The module contains the main application class.
"""

import asyncio
import logging
import threading
from typing import Self

from whisper.core.client import ClientConn
from whisper.settings import ClientSetting
from .ui import MainWindow
from .ui.layouts.root import Root
from .client import Client


logger = logging.getLogger(__name__)


class App(Client, MainWindow):
    """Main application (Frontend + Backend).

    Frontend is synchronous and is running on `MainThread` while the backend is
    àsynchronous and is running on `BackendThread`.

    Use `mainloop` to run the application.
    """

    def __init__(self,
        setting: ClientSetting | None = None,
        conn: ClientConn | None = None,
    ):
        """The `conn` object is used to connect with the servers."""
        Client.__init__(self, setting=setting, conn=conn)
        MainWindow.__init__(self)
        self.configure_app()
        self.thread = threading.Thread(target=self._run_backend, name="BackendThread")

    def configure_app(self):
        """
        Configure the application settings. Use this to setup custom
        configuration.
        """
        self.on_window_exit(self.shutdown)
        self.setup_root()

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
        # TODO - since error occurs here the application will close
        # But do not close the mainloop until backend shuts down
        try:
            MainWindow.mainloop(self, n)
        except KeyboardInterrupt:
            logger.info("Force closing the app! (KeyboardInterrput)")
        except Exception as ex:
            logger.exception(f"App.mainloop: {ex}")
        finally:
            self.shutdown()

    def _run_backend(self):
        """Starts the backend.

        NOTE: This should be running inside `App.thread`.
        """
        # TODO - it would be better if the error is handelled withn
        # eventloop so that there would be better control over running
        # eventloop
        try:
            asyncio.run(self.main())
        except BaseException as ex:
            logger.exception(f"App.run: {ex}")
            self.shutdown()

    def run(self):
        """Starts the backend thread."""
        if not self.thread.is_alive():
            self.thread.start()
            logger.info(f"{self.thread.name} is running!")
        else:
            logger.warning(f"{self.thread.name} is already running!")

    def shutdown(self):
        """Safely closes backend thread.."""
        if self.thread.is_alive():
            logger.debug("Shutting down backend")
            Client.shutdown(self)
            logger.debug(f"{self.thread.name} joining ...")
            self.thread.join()
            logger.debug(f"{self.thread.name} ended!")
        MainWindow.quit(self)
