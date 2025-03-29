"""
This module contains the client class which can communicate with server
and perform chat application related functions.
"""

import asyncio
from functools import cached_property
import logging
from typing import Tuple

from whisper.core.packet import Packet
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
        """Packetreceived from server."""
        return asyncio.Queue()

    @cached_property
    def sendq(self) -> asyncio.Queue[Packet]:
        """Packet send to server."""
        return asyncio.Queue()

    def server_address(self) -> Tuple[str, int]:
        """Provides remote server address."""
        return self.setting("host"), self.setting("port")

    def open_connection(self): # pylint: disable=arguments-differ
        """Connect to remote server."""
        host, port = self.server_address()
        logger.debug(f"Connecting to {(host, port)} ...")
        BaseClient.open_connection(self, host, port)
        logger.debug(f"Connection established with {(host, port)}!")

    async def main(self):
        """
        This defines the entry point of backend. It determines the
        different stges in backend.
        """
        self.open_connection()
        await self.process_tasks()
        self.close_connection()
        logger.debug("Disconnected!")

    def shutdown(self):
        """Close the application backend."""
        self.stop_running()

    def get_tasks(self):
        """Initial tasks."""
        return super().get_tasks() | {self.reader, self.writer}
