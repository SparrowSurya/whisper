"""
This module provides coroutines for client and server.
"""

import asyncio
from typing import Awaitable, Callable, Iterable, NoReturn, Sequence, Tuple

from whisper.core.packet import Packet, PacketKind # TODO - wrong imports
from whisper.core.server.client import ConnHandle
from whisper.utils.coro import handle_cancellation


@handle_cancellation("PacketReader")
async def packet_reader(
    queue: asyncio.Queue[Packet],
    reader: Callable[[], Awaitable[Packet]],
) -> NoReturn:
    """Reads the packet into queue (for client)."""
    while True:
        packet = await reader()
        await queue.put(packet)


@handle_cancellation("PacketWriter")
async def packet_writer(
    queue: asyncio.Queue[Packet],
    writer: Callable[[Packet], Awaitable[None]],
) -> NoReturn:
    """Writes the packet from queue (for client)."""
    while True:
        packet = await queue.get()
        await writer(packet)


@handle_cancellation("PacketHandler")
async def packet_handler(
    queue: asyncio.Queue[Packet],
    handler: Callable[[PacketKind], Callable[[bytes], None]],
) -> NoReturn:
    """Handles the packet from queue (for client)."""
    while True:
        packet = await queue.get()
        handle = handler(packet.kind) # type: ignore
        handle(packet.data)


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
        [PacketKind, Tuple[ConnHandle]],
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
