"""
This module provides client backend object which along with asynchronous event loop
manager provides easy way to manage asynchronous tasks, workers and other coroutines.
"""

import asyncio
from functools import cached_property

from whisper.client.base import BaseClient
from whisper.client.settings import Config
from whisper.client.workers import PacketReader, PacketWriter
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
        BaseClient.__init__(self, conn)
        EventLoop.__init__(self)
        self.logger = logger
        self.config = config

        self.reader = PacketReader(logger=self.logger)
        self.writer = PacketWriter(logger=self.logger)

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
        self.logger.debug(f"connecting to {(host, port)}")
        BaseClient.open_connection(self, host, port)
        self.logger.info("connectiion established")

    def close_connection(self):
        super().close_connection()
        self.logger.info("connection closed")

    def shutdown(self):
        """This marks the closing of running tasks and connection close."""
        self.logger.info("shutting down event loop")
        self.stop_running()

    def initial_tasks(self):
        return super().initial_tasks() | {
            self.reader(
                queue=self.recvq,
                reader=lambda: self.read(self.loop),
            ),
            self.writer(
                queue=self.sendq,
                writer=lambda p: self.write(p, self.loop),
            )
        }

    def init_connection(self, username: str):
        """This initialises the client on server side."""
        packet = InitPacket.create(username=username)
        self.schedule(self.sendq.put(packet))
