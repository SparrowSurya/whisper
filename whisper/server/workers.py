"""
This module provides coroutines for server.
"""

import asyncio
from typing import Awaitable, Callable, Iterable, NoReturn, Sequence, Tuple

from whisper.packet import Packet
from whisper.packet.v1 import PacketType
from whisper.server.connection import ConnHandle
from whisper.common.coro_handler import handle_cancellation


@handle_cancellation("ConnectionAcceptor")
async def connection_acceptor(
    acceptor: Callable[[], Awaitable[ConnHandle]],
    serve: Callable[[ConnHandle], None],
) -> NoReturn:
    """Accepts the incoming connections (for server)."""
    while True:
        conn = await acceptor()
        serve(conn)


@handle_cancellation("ConnectionReader")
async def connection_reader(
    conn: ConnHandle,
    reader: Callable[[ConnHandle], Awaitable[Packet]],
    queue: asyncio.Queue[Tuple[Packet, ConnHandle]],
):
    """Reads the packet from connection (for server)."""
    while not conn.close:
        packet = await reader(conn)
        await queue.put((packet, conn))


@handle_cancellation("ConnectionWriter")
async def connection_writer(
    writer: Callable[[Packet, ConnHandle], Awaitable[None]],
    queue: asyncio.Queue[Tuple[Packet, Iterable[ConnHandle]]],
) -> NoReturn:
    """Writes the packet to connections (for server)."""
    while True:
        packet, conns = await queue.get()
        for konn in conns:
            await writer(packet, konn)


@handle_cancellation("PacketDispatcher")
async def packet_dispatcher(
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
    """Handles the incoming packet into outgoing response packet."""
    while True:
        packet, conn = await recvq.get()
        handle = handler(packet.kind) # type: ignore
        responses = handle(packet.data, conn)

        if responses:
            for (packet, conns) in responses:
                await sendq.put((packet, conns))
