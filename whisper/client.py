"""
This module contains the client class which can communicate with server
and perform chat application related functions.
"""

import asyncio
from functools import cached_property
import logging

from whisper.core.packet import Packet
from whisper.core.client import BaseClient, ClientConn
from whisper.core.eventloop import EventLoop
from whisper.workers import packet_reader, packet_writer
from whisper.settings import Setting


logger = logging.getLogger(__name__)


class Client(BaseClient, EventLoop):
    """
    The class provides the asynchronous client backend for the chat
    application. It uses `EventLoop` to manage tasks, coroutines and
    workers.
    """

    def __init__(self, conn: ClientConn | None = None):
        """The `conn` object is used to connect with remote server."""
        BaseClient.__init__(self, conn)
        EventLoop.__init__(self)
        self.setting = Setting.from_defaults()

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

    async def main(self):
        """
        This defines the entry point of backend. It determines the
        series of events (lifecycle) in backend.
        """
        host, port = self.setting("host"), self.setting("port")
        logger.debug(f"Connecting to {(host, port)} ...")
        self.open_connection(host, port)
        logger.debug("Connection established!")
        await self.process_tasks()
        logger.debug("Disconnecting ...")
        self.close_connection()
        logger.debug("Disconnected!")

    def get_tasks(self):
        """Initial tasks."""
        return super().get_tasks() | {self.reader, self.writer}
