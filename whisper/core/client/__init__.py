"""
This module provides basic client functionality for communication with
server.
"""

import asyncio
import logging
from enum import StrEnum, auto
from functools import cached_property
from typing import Tuple

from whisper.core.packet import Packet
from whisper.core.workers import PacketReader, PacketWriter
from .connection import ClientConn


logger = logging.getLogger(__name__)


class ConnState(StrEnum):
    """Connection state."""

    NOT_CONNECTED = auto()
    CONNECTED = auto()
    DISCONNECTED = auto()


class BaseClient:
    """
    Base Client class for communicating with server. It manages the
    connection state. It stores incoming and outgoing packets using
    asynchronous queue.
    """

    def __init__(self, conn: ClientConn | None = None):
        """Requires a connection object to connect to server."""
        self.connection = conn or ClientConn()
        self.conn_state = ConnState.NOT_CONNECTED

        self.reader = PacketReader(
            queue=self.recvq,
            reader=self.aread,
        )
        self.writer = PacketWriter(
            queue=self.sendq,
            writer=self.awrite,
        )

    @cached_property
    def sendq(self) -> asyncio.Queue[Packet]:
        """Stores outgoing packets to server."""
        return asyncio.Queue()

    @cached_property
    def recvq(self) -> asyncio.Queue[Packet]:
        """Stores incoming packets from server."""
        return asyncio.Queue()

    @property
    def is_connected(self) -> bool:
        """
        This does not ensure that data can be sent or received over the
        connection.
        """
        return self.conn_state is ConnState.CONNECTED

    def server_address(self) -> Tuple[str, int]:
        """Provides the connected server address."""
        return self.connection.sock.getpeername()

    def connect(self, host: str, port: int):
        """Connect to server with given address."""
        logger.debug(f"Connecting to {(host, port)} ...")
        self.connection.open(host, port)
        self.conn_state = ConnState.CONNECTED
        logger.debug(f"Connected to {(host, port)}!")

    def disconnect(self):
        """Closes connection."""
        self.connection.close()
        self.conn_state = ConnState.DISCONNECTED
        logger.debug("Connection closed")

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
