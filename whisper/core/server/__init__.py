import asyncio
import logging
import socket


from .connection import ServerConn
from .handle import ConnHandle, Address  # noqa: F401
from .response import Response  # noqa: F401


logger = logging.getLogger(__name__)


class BaseServer:
    """
    Base server class capable of connecting and communicating to client.
    """

    def __init__(self, tcp_conn: ServerConn | None = None):
        """Initialises the tcp connection.

        Argument:
        * tcp_conn - server tcp connection.
        """
        self.connection = tcp_conn or ServerConn()

    async def accept(self, loop: asyncio.AbstractEventLoop) -> ConnHandle:
        """Accept incoming client connections."""
        sock, address = await self.connection.accept(loop)
        logger.debug(f"New connection: {address}")
        return ConnHandle(sock, Address(*address))

    async def aread(self,
        sock: socket.socket,
        n: int,
        loop: asyncio.AbstractEventLoop,
    ) -> bytes:
        """Read n bytes from connection."""
        return await self.connection.read(sock, n, loop)

    async def awrite(self,
        sock: socket.socket,
        data: bytes,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        """Write data to connection."""
        return await self.connection.write(sock, data, loop)

    def close(self, conn: ConnHandle):
        """Close the connection."""
        conn.sock.close()
        logger.debug(f"Closed connection: {conn.address}")

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
