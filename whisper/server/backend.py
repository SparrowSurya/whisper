"""
This module provides the server backend class.
"""

import asyncio
from functools import cached_property
from typing import Iterable, Dict, Tuple, NoReturn

from whisper.eventloop import EventLoop
from whisper.packet import Packet
from whisper.logger import Logger
from whisper.server.base import BaseServer
from whisper.server.connection import ConnHandle
# from .handlers import handlers
from whisper.typing import (
    TcpServer as _TcpServer,
    AsyncQueue as _AsyncQueue,
    Address as _Address,
)


class Server(BaseServer, EventLoop):
    """This class provides asynchronouse server backend for the chat applications."""

    def __init__(self, logger: Logger, conn: _TcpServer):
        """The connection object is used to accept client connections."""
        BaseServer.__init__(self, logger, conn)
        EventLoop.__init__(self)

        self.logger = logger
        self.clients: Dict[_Address, ConnHandle] = {}
        # self.handlers = {handler.packet_type: handler(self) for handler in handlers}

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
        error = EventLoop.run_main(self, self.main, host=host, port=port)
        if error is not None:
            if isinstance(error, KeyboardInterrupt):
                self.logger.info("keyboard interrupt")
            else:
                self.logger.exception(f"eventloop returned with error: {error!s}, 12")

    async def main(self, host: str, port: int): # type: ignore[override]
        self.start_server(host, port)
        await EventLoop.main(self)
        self.stop_server()

    def shutdown(self, sig: int | None = None):
        self.logger.info(f"Received signal: {sig}")
        EventLoop.stop_main(self)

    async def serve_coro(self, conn: ConnHandle):
        """Connection lifetime."""
        self.clients[conn.address] = conn
        await self.read_coro(conn)
        self.clients.pop(conn.address)

    def exception_handler(self, loop, context):
        self.logger.error(f"uncaught exception in eventloop task: {context}")

    async def handle_cancel(self, coro, name: str, *args, **kwargs):
        try:
            await coro(*args, **kwargs)
        except self.CancelledError:
            self.logger.info(f"{name} cancelled")
        except KeyboardInterrupt:
            self.logger.info(f"keyboard interrupt at {name}")
        except Exception as ex:
            self.logger.exception(f"error occured in {name}: {ex}")

    async def accept_coro(self) -> NoReturn:
        """Accepts incoming connection."""
        while True:
            conn = await self.accept(self.loop)
            self.create_task(self.serve_coro(conn))

    async def read_coro(self, conn: ConnHandle):
        """Reads incoming packets from connection."""
        while not conn.close:
            packet = await self.read(conn, self.loop)
            await self.recvq.put((packet, conn))

    async def write_coro(self) -> NoReturn:
        """Writes outgoing packet to connnections."""
        while True:
            packet, conns = await self.sendq.get()
            for conn in conns:
                await self.write(conn, packet, self.loop)

    # async def handler_coro(self) -> NoReturn:
    #     """Handles incoming packets from queue and writes outgoing packets to queue."""
    #     while True:
    #         packet, conn = await self.recvq.get()
    #         handler = self.handler[packet.kind]
    #         if responses := handler(packet, conn):
    #             for packet, conns in responses:
    #                 await self.sendq.put((packet, conns))

    def initial_tasks(self):
        """Initial tasks."""
        return super().initial_tasks() | {
            ("ConnectionAcceptor", self.accept_coro),
            ("ResponseWriter", self.write_coro),
            # ("PacketHandler", self.handler_coro),
        }
