"""
This module provides the server backend class.
"""

import asyncio
from functools import cached_property
from typing import Iterable, Set, Tuple

from whisper.eventloop import EventLoop
from whisper.packet import Packet
from whisper.logger import Logger
from whisper.server.base import BaseServer
from whisper.server.connection import ConnHandle
from whisper.server.workers import ConnAcceptor, ConnReader, ConnWriter, PacketHandler
from whisper.typing import (
    TcpServer as _TcpServer,
    AsyncQueue as _AsyncQueue,
)


class Server(BaseServer, EventLoop):
    """This class provides asynchronouse server backend for the chat applications."""

    def __init__(self, logger: Logger, conn: _TcpServer):
        """The connection object is used to accept client connections."""
        BaseServer.__init__(self, conn)
        EventLoop.__init__(self)

        self.logger = logger
        self.clients: Set[ConnHandle] = set()

        # self.acceptor = ConnAcceptor(logger=self.logger)
        # self.handler = PacketHandler(logger=self.logger)
        # self.writer = ConnWriter(logger=self.logger)

        # self.handlers = {} # TODO: packet handlers

    @cached_property
    def recvq(self) -> _AsyncQueue[Tuple[Packet, ConnHandle]]:
        """Packets received from connection."""
        return asyncio.Queue()

    @cached_property
    def sendq(self) -> _AsyncQueue[Tuple[Packet, Iterable[ConnHandle]]]:
        """Packets to be sent to connections."""
        return asyncio.Queue()

    def run(self, host: str, port: int):
        """Starts the server backend."""
        coro = self.start(host, port)
        error = EventLoop.run_coro(self, coro)
        if error is not None:
            if isinstance(error, KeyboardInterrupt):
                self.logger.info("keyboard interrupt")
            else:
                self.logger.exception(f"eventloop returned with error: {error!s}, 12")

    async def start(self, host: str, port: int):
        """Start the server."""
        self.start_server(host, port)
        self.logger.info(f"server running at {(host, port)}")
        await self.execute()
        self.stop_server()
        self.logger.info("server stopped")

    async def serve(self, conn: ConnHandle):
        """Connection lifetime."""
        self.logger.info(f"new connection from {conn.address}")
        self.clients.add(conn)
        reader = ConnReader(logger=self.logger)
        await reader(
            conn=conn,
            reader=lambda conn: self.read(conn, self.loop),
            queue=self.recvq,
        )
        self.clients.remove(conn)

    # def initial_tasks(self):
    #     """Initial tasks."""
    #     return super().initial_tasks() | {
    #         self.acceptor(
    #             acceptor=lambda: self.accept(self.loop),
    #             serve=lambda conn: self.schedule(self.serve(conn)),
    #         ),
    #         self.writer(
    #             writer=lambda packet, conn: self.write(conn, packet, self.loop),
    #             queue=self.sendq,
    #         ),
    #         self.handler(
    #             recvq=self.recvq,
    #             sendq=self.sendq,
    #             handler=self.get_handler, # TODO - not implemented
    #         ),
    #     }

    def exception_handler(self, loop, context):
        pass
