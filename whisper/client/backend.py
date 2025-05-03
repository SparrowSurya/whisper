"""
This module provides client backend object which along with asynchronous event loop
manager provides easy way to manage asynchronous tasks, workers and other coroutines.
"""

import struct
import asyncio
from functools import cached_property

from whisper.client.base import BaseClient
from whisper.client.settings import Config
from whisper.eventloop import EventLoop
from whisper.packet import Packet
from whisper.packet.v1 import InitPacket
from whisper.logger import Logger
from whisper.typing import (
    TcpClient as _TcpClient,
    AsyncQueue as _AsyncQueue,
    Address as _Address,
)


class Client(BaseClient, EventLoop):
    """
    It provides asynchronous client backend along with event loop management.
    """

    def __init__(self, logger: Logger, config: Config, conn: _TcpClient):
        """The `conn` object is used to connect with remote server."""
        BaseClient.__init__(self, logger, conn)
        EventLoop.__init__(self)
        self.config = config

    @cached_property
    def recvq(self) -> _AsyncQueue[Packet]:
        """Packet received from server."""
        return asyncio.Queue()

    @cached_property
    def sendq(self) -> _AsyncQueue[Packet]:
        """Packet send to server."""
        return asyncio.Queue()

    def server_address(self) ->_Address:
        """Provides remote server address depending upon the connection."""
        if self.is_connected:
            return BaseClient.server_address(self)
        return self.config.host, self.config.port

    def open_connection(self):
        """Connect to remote server."""
        host, port = self.server_address()
        BaseClient.open_connection(self, host, port)

    def initial_tasks(self):
        return super().initial_tasks() | {
            self.read_coro,
            self.write_coro,
        }

    def init_connection(self, username: str):
        """This initialises the client on server side."""
        packet = InitPacket.request(username=username)
        self.schedule(self.sendq.put(packet))

    async def read_coro(self):
        """Reads incoming packets from connection."""
        self.logger.info("read_coro running")
        while True:
            try:
                packet = await self.read(self.loop)
            except struct.error:
                self.logger.info("server disconnect")
                return self.stop_main()
            else:
                await self.recvq.put(packet)

    async def write_coro(self):
        """Writes outgoing packets to connection."""
        self.logger.info("write_coro running")
        while True:
            packet = await self.sendq.get()
            await self.write(packet, self.loop)
