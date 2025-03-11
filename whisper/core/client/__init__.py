"""
This module provides basic client functionality for communication with
server.
"""

import asyncio
import logging
from typing import Tuple

from whisper.core.packet import Packet
from whisper.core.workers import PacketReader, PacketWriter
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

        self.io_controller = asyncio.Condition()
        self.reader = PacketReader(
            queue=self.recvq,
            reader=self.aread,
            should_read=self.await_io,
        )
        self.writer = PacketWriter(
            queue=self.sendq,
            writer=self.awrite,
            should_write=self.await_io,
        )

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self.connection.is_connected


    # FIXME - WIP (reconnect)
    async def await_io(self) -> bool:
        """
        Controls the read/write on sockets based on the connection
        status. During socket disconnect it can be awaited until the
        underlying socket is again ready for io operations. Moreover,
        the return value provides information about the closing status.
        """
        async with self.io_controller:
            while not self.is_connected:
                await self.io_controller.wait()
            return True

    # FIXME - WIP (reconnect & unused)
    async def resume_io(self):
        """Resume the io operation awaited by `await_io`."""
        async with self.io_controller:
            self.io_controller.notify_all()

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
