"""
This module provides the server backend class.
"""

import asyncio
import logging

from .core.server import BaseServer, ServerConn
from .core.eventloop import EventLoop


logger = logging.getLogger(__name__)


class Server(BaseServer, EventLoop):
    """
    This class provides asynchronouse server backend for the chat
    applications.
    """

    def __init__(self, conn: ServerConn | None = None):
        """
        The connection object is used to accept client connections.
        """
        BaseServer.__init__(self, conn)
        EventLoop.__init__(self)

    def run(self, host: str, port: int):
        """Starts the server eventloop."""
        try:
            asyncio.run(self.start(host, port))
        except KeyboardInterrupt:
            logger.info("Force stopping the server!")
        except Exception as ex:
            logger.exception(ex)

    async def start(self, host: str, port: int):
        """Start the server."""
        self.start_server(host, port)
        await self.process_tasks()
        self.stop_server()
