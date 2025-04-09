"""
The module contains the client application object.
"""

import asyncio
import logging
import threading
from typing import Self

from whisper.client.backend import Client
from whisper.client.settings import ClientSetting
from whisper.client.tcp import TcpClient
from whisper.ui.window import MainWindow
from whisper.layouts.root import Root


logger = logging.getLogger(__name__)


class App(Client, MainWindow):
    """Main application (Frontend + Backend).

    Frontend is synchronous and is running on `MainThread` while the backend is
    asynchronous and is running on `BackendThread`.

    Use `mainloop` to run the application.
    """

    def __init__(self,
        title: str,
        setting: ClientSetting | None = None,
        conn: TcpClient | None = None,
    ):
        """The `conn` object is used to connect with the servers."""
        Client.__init__(self, setting=setting, conn=conn)
        MainWindow.__init__(self)
        self.thread = threading.Thread(target=self._run_backend, name="BackendThread")
        self.title(title)
        self.configure_app()

    def configure_app(self):
        """Configure the application settings. Use this to setup custom
        configuration."""
        self.on_window_exit(self.shutdown)
        self.setup_root()
        self.minsize(200, 200)

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

    def _run_backend(self): # TODO - error handler
        """Starts the backend.

        NOTE: This should be running inside `App.thread`.
        """
        try:
            asyncio.run(self.main())
        except BaseException as ex:
            logger.exception(f"App.run: {ex}")
            self.shutdown()

    def run(self):
        """Starts the backend thread."""
        if not self.thread.is_alive():
            self.thread.start()

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
        MainWindow.quit(self)

    def init_connection(self): # TODO
        """Opens a dialogue box for required details."""
        # form = ConnInitForm(self)
        # callback = lambda **kw: Client.init_connection(self, **kw)  # noqa: E731
        # form.on_submit(callback)
