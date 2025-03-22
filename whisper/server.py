"""
This module provides the server backend class.
"""

import asyncio
from functools import cached_property
import logging
from typing import Iterable, Set, Tuple

from whisper.core.server import BaseServer, ServerConn
from whisper.core.eventloop import EventLoop
from whisper.workers import (
    connection_acceptor, connection_reader,
    connection_writer, packet_dispatcher
)
from .core.server.client import ConnHandle
from .core.packet import Packet


logger = logging.getLogger(__name__)


class Server(BaseServer, EventLoop):
    """
    This class provides asynchronouse server backend for the chat
    applications.
    """

    def __init__(self, conn: ServerConn | None = None):
        """
        The connection object is used to accept client connections.
        """
        BaseServer.__init__(self, conn)
        EventLoop.__init__(self)

        self.clients: Set[ConnHandle] = set()

        self.acceptor = connection_acceptor(
            acceptor=lambda: self.accept(self.loop),
            serve=lambda conn: self.schedule(self.serve(conn)),
        )

        self.dispatcher = packet_dispatcher(
            recvq=self.recvq,
            sendq=self.sendq,
            handler=self.handler, # TODO - not implemented
        )

        self.writer = connection_writer(
            writer=lambda packet, conn: self.write(conn, packet, self.loop),
            queue=self.sendq,
        )

    @cached_property
    def recvq(self) -> asyncio.Queue[Tuple[Packet, ConnHandle]]:
        """Packets received from connection."""
        return asyncio.Queue()

    @cached_property
    def sendq(self) -> asyncio.Queue[Tuple[Packet, Iterable[ConnHandle]]]:
        """Packets to be sent to connections."""
        return asyncio.Queue()

    def run(self, host: str, port: int):
        """Starts the server eventloop."""
        try:
            asyncio.run(self.start(host, port))
        except KeyboardInterrupt:
            logger.info("Force stopping the server!")
        except Exception as ex:
            logger.exception(ex)

    async def start(self, host: str, port: int):
        """Start the server."""
        self.start_server(host, port)
        await self.process_tasks()
        self.stop_server()

    async def serve(self, conn: ConnHandle):
        """Connection lifetime."""
        logger.info(f"New Connection: {conn.address}")
        self.clients.add(conn)
        await connection_reader(
            conn=conn,
            reader=lambda conn: self.read(conn, self.loop),
            queue=self.recvq,
        )
        self.clients.remove(conn)

    def get_tasks(self):
        """Initial tasks."""
        return super().get_tasks() | {self.acceptor, self.writer}
