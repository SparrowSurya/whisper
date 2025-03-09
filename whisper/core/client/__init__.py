"""
This module provides basic client functionality for communication with
server.
"""

import asyncio
import logging
from typing import Awaitable, Callable, Tuple

from whisper.core.packet import Packet
from whisper.utils.decorators import aworker
from .connection import ClientConn


logger = logging.getLogger(__name__)


class BaseClient:
    """
    Base Client class for communicating with server. It manages
    incoming and outgoing packets using asynchronous queue. It uses
    `Packet` as means of massages.
    """

    def __init__(self, tcp_conn: ClientConn | None = None):
        """Requires a connection object to connect to server."""
        self.connection = tcp_conn or ClientConn()
        self.sendq: asyncio.Queue[Packet] = asyncio.Queue()
        self.recvq: asyncio.Queue[Packet] = asyncio.Queue()

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self.connection.is_connected

    def server_address(self) -> Tuple[str, int]:
        """Provides the connected server address."""
        return self.connection.sock.getpeername()

    def connect(self, host: str, port: int):
        """Connect to server with given address."""
        logger.debug(f"Connecting to {(host, port)} ...")
        self.connection.connect(host, port)
        logger.debug(f"Connected to {(host, port)}!")

    def disconnect(self):
        """Closes connection."""
        self.connection.disconnect()
        logger.debug("Connection closed")

    @aworker("PacketReader", logger=logger) # TODO - use handler
    async def arecv(self, reader: Callable[[int], Awaitable[bytes]]):
        """Coroutine reading incoming packets from the server."""
        while True:
            packet = await Packet.from_stream(reader)
            await self.recvq.put(packet)
            logger.debug(f"Received: {packet!r}")

    @aworker("PacketWriter", logger=logger) # TODO - use handler
    async def asend(self, writer: Callable[[bytes], Awaitable[None]]):
        """Coroutine writing packets to the server."""
        while True:
            packet = await self.sendq.get()
            data = packet.to_stream()
            await writer(data)
            logger.debug(f"Sent: {packet!r}")

    async def aread(self,
        n: int,
        loop: asyncio.AbstractEventLoop,
    ) -> bytes:
        """Read `n` bytes from server."""
        return await self.connection.read(n, loop)

    async def awrite(self,
        data: bytes,
        loop: asyncio.AbstractEventLoop,
    ):
        """Write `data` to server."""
        return await self.connection.write(data, loop)
