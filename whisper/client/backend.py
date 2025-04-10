"""
This module provides client backend object which along with asynchronous event loop
manager provides easy way to manage asynchronous tasks, workers and other coroutines.
"""

import asyncio
from functools import cached_property
from typing import Tuple

from whisper.client.base import BaseClient
from whisper.client.settings import ClientSetting
from whisper.client.tcp import TcpClient
from whisper.client.workers import PacketReader, PacketWriter
from whisper.eventloop import EventLoop
from whisper.packet import Packet
from whisper.packet.v1 import InitPacket
from whisper.logger import Logger


class Client(BaseClient, EventLoop):
    """
    It provides asynchronous client backend along with event loop management.
    """

    def __init__(self,
        logger: Logger,
        setting: ClientSetting | None = None,
        conn: TcpClient | None = None,
    ):
        """The `conn` object is used to connect with remote server."""
        BaseClient.__init__(self, conn)
        EventLoop.__init__(self)
        self.logger = logger
        self.setting = setting or ClientSetting.defaults()

        self.reader = PacketReader(logger=self.logger)
        self.writer = PacketWriter(logger=self.logger)

    @cached_property
    def recvq(self) -> asyncio.Queue[Packet]:
        """Packet received from server."""
        return asyncio.Queue()

    @cached_property
    def sendq(self) -> asyncio.Queue[Packet]:
        """Packet send to server."""
        return asyncio.Queue()

    def server_address(self) -> Tuple[str, int]:
        """Provides remote server address depending upon the connection."""
        if self.is_connected:
            return BaseClient.server_address(self)
        return self.setting("host"), self.setting("port")

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
