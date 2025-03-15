"""
This module provides the basic server functionality to manage clients
and communication.
"""

import asyncio
import logging

from whisper.core.packet import Packet
from .connection import ServerConn
from .handle import ConnHandle, Address


logger = logging.getLogger(__name__)


class BaseServer:
    """
    Base server class for communicating with clients. It provides
    asynchronous methods for reading, writing and accepting.
    """

    def __init__(self, tcp_conn: ServerConn | None = None):
        """Initialise connection."""
        self.connection = tcp_conn or ServerConn()

    async def accept(self, loop: asyncio.AbstractEventLoop) -> ConnHandle:
        """Accept incoming client connections."""
        sock, address = await self.connection.accept(loop)
        logger.debug(f"Accepted: {address}")
        return ConnHandle(sock, Address(*address))

    async def read(self,
        conn: ConnHandle,
        loop: asyncio.AbstractEventLoop,
    ) -> Packet:
        """Read `n` bytes from connection."""
        reader = lambda n: self.connection.read(conn.sock, n, loop)  # noqa: E731
        return await Packet.from_stream(reader)

    async def write(self,
        conn: ConnHandle,
        packet: Packet,
        loop: asyncio.AbstractEventLoop,
    ):
        """Write `data` to connection."""
        data = packet.to_stream()
        return await self.connection.write(conn.sock, data, loop)

    def close(self, conn: ConnHandle):
        """Close the connection."""
        conn.sock.close()
        logger.debug(f"Closed: {conn.address}")

    @property
    def is_serving(self) -> bool:
        """Check is server is running."""
        return self.connection.is_serving

    def start_server(self, host: str, port: int):
        """Start the server on given address."""
        self.connection.start(host, port)
        logger.info(f"Server running on {self.connection.address()}")

    def stop_server(self):
        """Close the server."""
        self.connection.stop()
        logger.info("Server stopped.")
