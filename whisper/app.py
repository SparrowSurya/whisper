import asyncio
import logging
import threading
from typing import Self

from whisper.core.client import ClientConn
from .ui import MainWindow
from .client import Client


logger = logging.getLogger(__name__)


class Application(Client, MainWindow):
    """Main application."""

    def __init__(self, conn: ClientConn | None = None):
        Client.__init__(self, conn)
        MainWindow.__init__(self)
        self.setup()
        self.thread = threading.Thread(target=self.run, name="BackendThread")

    def setup(self):
        """Configure all the setup."""
        self.on_window_exit(self.shutdown)
        self.setup_root()

    @property
    def app(self) -> Self:
        """Self refrence."""
        return self

    def mainloop(self):
        """Run the application. This should be running in main thread."""
        logger.debug("Application running")
        try:
            MainWindow.mainloop(self)
        except KeyboardInterrupt:
            logger.debug("Caught KeyboardInterrput")
        except Exception as error:
            logger.exception(f"An exception occured: {error}")
        finally:
            self.shutdown()
            logger.debug("Application exited")

    def run(self):
        """Run the client backend. This should be running in a seperate
        thread. Do not call this method directly."""
        try:
            asyncio.run(self.main())
        except BaseException as error:
            logger.exception(f"An exception occured: {error}")
            self.shutdown()

    def run_thread(self):
        """Invoke the client backend."""
        if not self.thread.is_alive():
            logger.debug(f"{self.thread.name} started")
            self.thread.start()
        else:
            logger.warning(f"Attempted to run {self.thread.name} twice")

    def shutdown(self):
        """Close application. Safely handles running thread."""
        logger.debug("Shutting down application")
        if self.thread.is_alive():
            self.stop()
            logger.debug(f"Waiting thread join: {self.thread.name}")
            self.thread.join()
            logger.debug(f"Thread finished: {self.thread.name}")
        MainWindow.quit(self)
