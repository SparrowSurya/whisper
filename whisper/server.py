"""
This module provides the server object.
"""

import asyncio
import logging
from typing import Set, Coroutine, Any

from .core.server import BaseServer, ServerConn
from .core.server.handle import ConnHandle
from .core.eventloop import EventLoop


logger = logging.getLogger(__name__)


class Server(BaseServer, EventLoop):
    """
    This class provides asynchronouse server backend actions for the
    client app.
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
        finally:
            self.stop_running()

    async def start(self, host: str, port: int):
        """Start the server."""
        self.start_server(host, port)
        await self.process_tasks()
        self.stop_server()

    def get_tasks(self) -> Set[Coroutine[Any, Any, Any]]:
        """Provides a set of tasks to start with."""
        return {self.acceptor()}

    async def handle(self, conn: ConnHandle):
        """Handles the connection lifetime."""
        self.conns.add(conn)
        try:
            await self.serve(conn)
        except Exception as ex:
            logger.exception(ex)
        finally:
            conn.sock.close()
            self.conns.remove(conn)

    async def serve(self, conn: ConnHandle):
        """Handles the communication with connection.."""

    def stop_server(self):
        """Close the connection and stop."""
        logger.info("Stopping server ...")
        for conn in self.conns:
            self.close(conn)
        return super().stop_server()
