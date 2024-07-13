import asyncio
from typing import Any, Coroutine

from ..logger import logger
from .connection import ServerConnection
from .handle import ConnectionHandle


class BaseServer:
    """
    The class provides the basic functionality for server. Its purpose
    is to serve the minimum essential functions.
    """

    def __init__(self, connection: ServerConnection | None = None):
        """Initialises the connection object.

        Arguments:
        * connection - object to manage the server connection.
        """
        self.connection = connection or ServerConnection()
        self._loop = None

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Running asyncio event loop. If is not set then the loop is
        set ro running event loop,

        Raises:
        * RuntimeError - if not event loop was found.
        """
        if self._loop is None:
            self.loop = asyncio.get_running_loop()
        return self._loop

    @loop.setter
    def loop(self, loop: asyncio.AbstractEventLoop):
        """Set asyncio event loop."""
        self._loop = loop

    async def accept(self) -> ConnectionHandle:
        """Accept the incoming conection. Returns a dataclass wrapper
        object around the connection."""
        sock, address = await self.connection.accept(self.loop)
        logger.info(f"New connection: {address}")
        return ConnectionHandle(sock, address)

    async def read(self, conn: ConnectionHandle, n: int) -> Coroutine[Any, Any, bytes]:
        """Read n bytes from connection."""
        return await self.connection.read(conn.sock, n, self.loop)

    async def write(self, conn: ConnectionHandle, data: bytes):
        """Write data to connection."""
        return await self.connection.write(conn.sock, data, self.loop)

    def close(self, conn: ConnectionHandle):
        """Close the connection."""
        conn.sock.close()
        logger.info(f"Closed connection: {conn.address}")

    @property
    def is_serving(self) -> bool:
        return self.connection.is_serving

    def start_server(self, host: str, port: int):
        """Start the server.

        Arguments:
        * host - hostname/ip address of the server.
        * port - port address.

        Raies:
        * OSError - if the address is already in use.
        * RuntimeError - server is already serving.
        """
        self.connection.start(host, port)
        logger.info(f"Server running on {self.connection.address}")

    def stop_server(self):
        """Close the server."""
        self.connection.stop()
        logger.info("Server stopped.")
