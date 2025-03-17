"""
This module contains the client class which can communicate with server
and perform chat application related functions.
"""

import logging

from .core.client import BaseClient, ClientConn
from .core.eventloop import EventLoop
from .settings import Setting


logger = logging.getLogger(__name__)


class Client(BaseClient, EventLoop):
    """
    The class provides the asynchronous client backend for the chat
    application. It uses `EventLoop` to manage tasks, coroutines and
    workers.
    """

    def __init__(self, conn: ClientConn | None = None):
        """The `conn` object is used to connect with remote server."""
        BaseClient.__init__(self, conn)
        EventLoop.__init__(self)
        self.setting = Setting.from_defaults()

    async def main(self):
        """
        This defines the entry point of backend. It determines the
        series of events (lifecycle) in backend.
        """
        host, port = self.setting("host"), self.setting("port")
        logger.debug(f"Connecting to {(host, port)} ...")
        self.open_connection(host, port)
        logger.debug("Connection established!")
        await self.process_tasks()
        logger.debug("Disconnecting ...")
        self.close_connection()
        logger.debug("Disconnected!")
