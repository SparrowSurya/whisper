"""
This module provides coroutines for server.
"""

import asyncio
from typing import Awaitable, Callable, Iterable, NoReturn, Sequence, Tuple

from whisper.worker import Worker
from whisper.packet import Packet
from whisper.packet.v1 import PacketType
from whisper.server.connection import ConnHandle


class ConnAcceptor(Worker):
    """Accepts incoming connection and serves them."""

    async def work(self,
        acceptor: Callable[[], Awaitable[ConnHandle]],
        serve: Callable[[ConnHandle], None],
    ) -> NoReturn:
        while True:
            conn = await acceptor()
            serve(conn)


class ConnReader(Worker):
    """Reads incoming packet from connection into queue."""

    async def work(self,
        conn: ConnHandle,
        reader: Callable[[ConnHandle], Awaitable[Packet]],
        queue: asyncio.Queue[Tuple[Packet, ConnHandle]],
    ):
        while not conn.close:
            packet = await reader(conn)
            await queue.put((packet, conn))


class ConnWriter(Worker):
    """Writes the packet to connection from queue"""

    async def work(
        writer: Callable[[Packet, ConnHandle], Awaitable[None]],
        queue: asyncio.Queue[Tuple[Packet, Iterable[ConnHandle]]],
    ) -> NoReturn:
        while True:
            packet, conns = await queue.get()
            for konn in conns:
                await writer(packet, konn)


class PacketHandler(Worker):
    """Handles each request packet and queues its response."""

    async def work(
        recvq: asyncio.Queue[Tuple[Packet, ConnHandle]],
        sendq: asyncio.Queue[Tuple[Packet, Iterable[ConnHandle]]],
        handler: Callable[
            [PacketType, Tuple[ConnHandle]],
            Callable[
                [bytes, ConnHandle],
                Sequence[Tuple[Packet, Iterable[ConnHandle]]] | None
            ]
        ],
    ) -> NoReturn:
        while True:
            packet, conn = await recvq.get()
            handle = handler(packet.kind) # type: ignore
            responses = handle(packet.data, conn)

            if responses:
                for (packet, conns) in responses:
                    await sendq.put((packet, conns))
