"""
This module provides coroutines for client.
"""

import asyncio
from typing import Awaitable, Callable, NoReturn

from whisper.common.coro_handler import handle_cancellation
from whisper.packet import Packet
from whisper.packet.v1 import PacketType


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
    handler: Callable[[PacketType], Callable[[bytes], None]],
) -> NoReturn:
    """Handles the packet from queue (for client)."""
    while True:
        packet = await queue.get()
        handle = handler(packet.kind) # type: ignore
        handle(packet.data)
