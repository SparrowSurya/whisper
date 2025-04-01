"""
This module contains the client class which can communicate with server
and perform chat application related functions.
"""

import asyncio
from functools import cached_property
import logging
from typing import Tuple

from whisper.core.packet import Packet
from whisper.core.packet.v1 import InitPacket
from whisper.core.client import BaseClient, ClientConn
from whisper.core.eventloop import EventLoop
from whisper.workers import packet_reader, packet_writer
from whisper.settings import ClientSetting


logger = logging.getLogger(__name__)


class Client(BaseClient, EventLoop):
    """
    The class provides the asynchronous client backend for the chat
    application. It uses `EventLoop` to manage tasks, coroutines and
    workers.
    """

    def __init__(self,
        setting: ClientSetting | None = None,
        conn: ClientConn | None = None,
    ):
        """The `conn` object is used to connect with remote server."""
        BaseClient.__init__(self, conn)
        EventLoop.__init__(self)
        self.setting = setting or ClientSetting.defaults()

        self.reader = packet_reader(
            queue=self.recvq,
            reader=lambda: self.read(self.loop),
        )
        self.writer = packet_writer(
            queue=self.sendq,
            writer=lambda p: self.write(p, self.loop),
        )

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
        logger.debug(f"Connecting to {(host, port)} ...")
        BaseClient.open_connection(self, host, port)
        logger.debug(f"Connection established with {(host, port)}!")

    def shutdown(self):
        """This marks the closing of running tasks and connection close."""
        self.stop_running()

    def initial_tasks(self):
        return super().initial_tasks() | {self.reader, self.writer}

    def init_connection(self, username: str):
        """This initialises the client on server side."""
        packet = InitPacket.create(username=username)
        self.schedule(self.sendq.put(packet))
