"""
This module provides client backend object which along with asynchronous event loop
manager provides easy way to manage asynchronous tasks, workers and other coroutines.
"""

import struct
import asyncio
import logging
from functools import cached_property

from whisper.client.base import BaseClient
from whisper.client.settings import Config
from whisper.eventloop import EventLoop
from whisper.packet import Packet
from whisper.packet.v1 import InitV1Packet
from whisper.common import Address
from whisper.typing import (
    TcpClient as _TcpClient,
    AsyncQueue as _AsyncQueue,
)


logger = logging.getLogger(__name__)

class Client(BaseClient, EventLoop):
    """
    It provides asynchronous client backend along with event loop management.
    """

    def __init__(self, config: Config, conn: _TcpClient):
        """The `conn` object is used to connect with remote server."""
        BaseClient.__init__(self, conn)
        EventLoop.__init__(self)
        self.cfg = config

    @cached_property
    def recvq(self) -> _AsyncQueue[Packet]:
        """Packet received from server."""
        return asyncio.Queue()

    @cached_property
    def sendq(self) -> _AsyncQueue[Packet]:
        """Packet send to server."""
        return asyncio.Queue()

    def server_address(self) -> Address:
        """Provides remote server address depending upon the connection."""
        if self.is_connected:
            return BaseClient.server_address(self)
        return self.cfg.host, self.cfg.port

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
        packet = InitV1Packet.request(username=username)
        self.schedule(self.sendq.put(packet))

    async def read_coro(self):
        """Reads incoming packets from connection."""
        logger.info("read_coro running")
        run = True
        while run:
            try:
                packet = await self.read(self.loop)
            except struct.error:
                run = False
                logger.info("server disconnect")
            except self.CancelledError:
                run = False
                logger.info("read_coro task cancelled")
            except Exception:
                run = False
                logger.exception("exception occured while reading packet")
            else:
                await self.recvq.put(packet)
        self.stop_main()
        logger.info("read_coro exited")

    async def write_coro(self):
        """Writes outgoing packets to connection."""
        logger.info("write_coro running")
        run = True
        while run:
            packet = await self.sendq.get()
            try:
                await self.write(packet, self.loop)
            except self.CancelledError:
                run = False
                logger.info("write_coro task cancelled")
            except Exception:
                run = False
                logger.exception("exception occured while writing packet")
        logger.info("write_coro exited")
