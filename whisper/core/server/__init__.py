"""
This module provides the basic server functionality to manage clients
and communication.
"""

import asyncio
import logging
from socket import socket
from functools import cached_property
from typing import Set, Tuple

from whisper.core.packet import Packet
from ..workers import AcceptHandler
from .response import Response
from .connection import ServerConn
from .handle import ConnHandle


logger = logging.getLogger(__name__)


class BaseServer:
    """
    Base server class for communicating with clients. It provides
    asynchronous methods for reading, writing and accepting.
    """

    def __init__(self, conn: ServerConn | None = None):
        """Initialise connection."""
        self.connection = conn or ServerConn()
        self.conns: Set[ConnHandle] = set()

        self.acceptor = AcceptHandler(
            handler=self.handle,
            acceptor=self.accept, # type: ignore
        )

    @cached_property
    def sendq(self) -> asyncio.Queue[Response]:
        """Stores outgoing response packets to clients."""
        return asyncio.Queue()

    @cached_property
    def recvq(self) -> asyncio.Queue[Packet]:
        """Stores incoming packets from clients."""
        return asyncio.Queue()

    async def accept(self,
        loop: asyncio.AbstractEventLoop,
    ) -> Tuple[socket, Tuple[str, int]]:
        """Accept incoming client connections."""
        sock, address = await self.connection.accept(loop)
        logger.debug(f"Accepted: {address}")
        return sock, address

    async def read(self,
        sock: socket,
        loop: asyncio.AbstractEventLoop,
    ) -> Packet:
        """Read `n` bytes from connection."""
        reader = lambda n: self.connection.read(sock, n, loop)  # noqa: E731
        return await Packet.from_stream(reader)

    async def write(self,
        sock: socket,
        packet: Packet,
        loop: asyncio.AbstractEventLoop,
    ):
        """Write `data` to connection."""
        data = packet.to_stream()
        return await self.connection.write(sock, data, loop)

    def close(self, conn: ConnHandle):
        """Close the connection."""
        conn.sock.close()
        logger.debug(f"Closed connection: {conn.address}")


    def start_server(self, host: str, port: int):
        """Start the server on given address."""
        self.connection.start(host, port)
        logger.info(f"Server running on {self.connection.address()}")

    def stop_server(self):
        """Close the server."""
        self.connection.stop()
        logger.info("Server stopped.")

    async def handle(self, conn: ConnHandle):
        """Handles the new connection."""
        self.conns.add(conn)
        await self.serve(conn)
        conn.sock.close()
        self.conns.remove(conn)

    async def serve(self, conn: ConnHandle):
        """Serve the connection."""
