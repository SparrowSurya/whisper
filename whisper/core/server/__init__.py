"""
This module provides the basic server functionality to manage clients
and communication.
"""

import asyncio

from whisper.core.packet import Packet
from .connection import ServerConn
from .client import ConnHandle


class BaseServer:
    """
    Base server class for communicating with clients. It provides
    asynchronous methods for reading, writing and accepting.
    """

    def __init__(self, conn: ServerConn | None = None):
        """Initialise connection."""
        self.connection = conn or ServerConn()

    async def accept(self,
        loop: asyncio.AbstractEventLoop,
    ) -> ConnHandle:
        """Accept incoming client connections."""
        sock, address = await self.connection.accept(loop)
        return ConnHandle(sock, address) # type: ignore

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

    def start_server(self, host: str, port: int):
        """Start the server on given address."""
        self.connection.start(host, port)

    def stop_server(self):
        """Close the server."""
        self.connection.stop()
