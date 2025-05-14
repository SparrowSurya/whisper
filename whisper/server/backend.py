"""
This module provides the server backend class.
"""

import struct
import asyncio
import logging
from functools import cached_property
from typing import Iterable, Dict, Tuple, NoReturn

from whisper.eventloop import EventLoop
from whisper.common import Address
from whisper.packet import Packet
from whisper.packet.v1 import ExitV1Packet, ExitReason, Status
from whisper.server.base import BaseServer
from whisper.server.connection import ConnHandle
from whisper.server.handlers import Handlers
from whisper.typing import (
    TcpServer as _TcpServer,
    AsyncQueue as _AsyncQueue,
)


logger = logging.getLogger(__name__)

class Server(BaseServer, EventLoop):
    """This class provides asynchronouse server backend for the chat applications."""

    def __init__(self, conn: _TcpServer):
        """The connection object is used to accept client connections."""
        BaseServer.__init__(self, conn)
        EventLoop.__init__(self)

        self.clients: Dict[Address, ConnHandle] = {}
        self.handlers = {version: {
            handler.unique_key(): handler(self) for handler in Handlers[version]
        } for version in Handlers.keys()}

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
        if EventLoop.run_main(self, self.main, host=host, port=port) is None:
            logger.info("eventloop exited")
        else:
            logger.exception("eventloop exited due to exception")

    async def main(self, host: str, port: int): # type: ignore[override]
        self.start_server(host, port)
        await EventLoop.main(self)
        exit_packet = ExitV1Packet.response(ExitReason.SELF_EXIT, Status.SUCCESS)
        for address, conn in self.clients:
            await self.write(conn, exit_packet, self.loop)
            logger.info(f"sent {exit_packet!r} to {address}")
        self.stop_server()

    def shutdown(self, sig: int | None = None):
        logger.info(f"received signal: {sig}")
        EventLoop.stop_main(self)

    def serve_coro(self, conn: ConnHandle) -> asyncio.Task:
        """Handles the connection to be served.."""
        self.clients[conn.address] = conn
        task = self.create_task(self.read_coro(conn))
        conn.data["read_coro"] = task
        task.add_done_callback(lambda _: self.close(conn))
        return task

    def close(self, conn: ConnHandle):
        task = conn.data.pop("read_coro", None)
        if task and not task.done():
            task.cancel()
        self.clients.pop(conn.address)
        return BaseServer.close(self, conn)

    async def handle_cancel(self, coro, name: str, *args, **kwargs):
        try:
            await coro(*args, **kwargs)
        except self.CancelledError:
            logger.info(f"{name} cancelled")
        except KeyboardInterrupt:
            logger.info(f"keyboard interrupt at {name}")
        except Exception as ex:
            logger.exception(f"error occured in {name}: {ex}")

    async def accept_coro(self) -> NoReturn:
        """Accepts incoming connection."""
        logger.info("accept_coro running")
        run = True
        while run:
            try:
                conn = await self.accept(self.loop)
            except self.CancelledError:
                run = False
                logger.info("accept_coro cancelled")
            except Exception:
                run = False
                logger.exception("exception occure while running accept_coro")
            else:
                self.serve_coro(conn)
        logger.info("accept_coro exited")

    async def read_coro(self, conn: ConnHandle):
        """Reads incoming packets from connection."""
        logger.info(f"read_coro running for {conn.address}")
        while not conn.close:
            try:
                packet = await self.read(conn, self.loop)
            except struct.error:
                conn.close = True
                logger.info(f"{conn.address} diconnected")
            except self.CancelledError:
                conn.close = True
                logger.info(f"read_coro task cancelled for {conn.address}")
            except Exception as ex:
                logger.exception(
                    f"uncaught exception while serving {conn.address}: {ex}")
            else:
                await self.recvq.put((packet, conn))
        logger.info(f"read_coro stopped for {conn.address}")

    async def write_coro(self) -> NoReturn:
        """Writes outgoing packet to connnections."""
        logger.info("write_coro running")
        run = True
        while run:
            packet, conns = await self.sendq.get()
            for conn in conns:
                try:
                    await self.write(conn, packet, self.loop)
                except self.CancelledError:
                    run = False
                    logger.info("write_coro task cancelled")
                except Exception:
                    run = False
                    conn.close = True
                    logger.exception("exception occure whiel running write_coro")
        logger.info("write_coro exited")

    async def handler_coro(self) -> NoReturn:
        """Handles incoming packets from queue and writes outgoing packets to queue."""
        logger.info("handler_coro running")
        while True:
            packet, conn = await self.recvq.get()
            handler = self.handlers[packet.version()][packet.unique_key()]
            if responses := handler(packet, conn):
                for packet, conns in responses:
                    await self.sendq.put((packet, conns))

    def initial_tasks(self):
        """Initial tasks."""
        return super().initial_tasks() | {
            self.accept_coro,
            self.write_coro,
            self.handler_coro,
        }
