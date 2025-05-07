"""
This module provides the basic server functionality to manage clients and communication.
"""

import logging

from whisper.packet import Packet
from whisper.server.connection import ConnHandle
from whisper.typing import (
    TcpServer as _TcpServer,
    EventLoop as _EventLoop,
)


logger = logging.getLogger(__name__)

class BaseServer:
    """Base server class for communicating with clients. It provides asynchronous
    methods for reading, writing and accepting."""

    def __init__(self, conn: _TcpServer):
        self.conn = conn

    async def accept(self, loop: _EventLoop) -> ConnHandle:
        """Accept incoming client connections."""
        sock, address = await self.conn.accept(loop)
        logger.info(f"accepted connection from {address}")
        return ConnHandle(sock, address, {}) # type: ignore

    async def read(self, conn: ConnHandle, loop: _EventLoop) -> Packet:
        """Read `n` bytes from connection."""
        reader = lambda n: self.conn.read(conn.sock, n, loop)  # noqa: E731
        packet = await Packet.from_stream(reader)
        logger.debug(f"received {packet!r} from {conn.address}")
        return packet

    async def write(self, conn: ConnHandle, packet: Packet, loop: _EventLoop):
        """Write `data` to connection."""
        data = packet.to_stream()
        await self.conn.write(conn.sock, data, loop)
        logger.debug(f"sent {packet!r} to {conn.address}")

    def close(self, conn: ConnHandle):
        """Close the connection."""
        logger.info(f"closed connection with {conn.address}")
        conn.sock.close()

    def start_server(self, host: str, port: int):
        """Start the server on given address."""
        self.conn.start(host, port)
        logger.info(f"server running at {host}:{port}")

    def stop_server(self):
        """Close the server."""
        self.conn.stop()
        logger.info("server closed")
