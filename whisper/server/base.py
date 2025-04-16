"""
This module provides the basic server functionality to manage clients and communication.
"""

from whisper.packet import Packet
from whisper.server.connection import ConnHandle
from whisper.typing import (
    TcpServer as _TcpServer,
    EventLoop as _EventLoop,
)


class BaseServer:
    """Base server class for communicating with clients. It provides asynchronous
    methods for reading, writing and accepting."""

    def __init__(self, conn: _TcpServer):
        """Initialise connection."""
        self.conn = conn

    async def accept(self, loop: _EventLoop) -> ConnHandle:
        """Accept incoming client connections."""
        sock, address = await self.conn.accept(loop)
        return ConnHandle(sock, address) # type: ignore

    async def read(self, conn: ConnHandle, loop: _EventLoop) -> Packet:
        """Read `n` bytes from connection."""
        reader = lambda n: self.conn.read(conn.sock, n, loop)  # noqa: E731
        return await Packet.from_stream(reader)

    async def write(self, conn: ConnHandle, packet: Packet, loop: _EventLoop):
        """Write `data` to connection."""
        data = packet.to_stream()
        return await self.conn.write(conn.sock, data, loop)

    def close(self, conn: ConnHandle):
        """Close the connection."""
        conn.sock.close()

    def start_server(self, host: str, port: int):
        """Start the server on given address."""
        self.conn.start(host, port)

    def stop_server(self):
        """Close the server."""
        self.conn.stop()
