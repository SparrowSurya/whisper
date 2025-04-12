"""
This module provides wokers for client.
"""

import asyncio
from typing import Awaitable, Callable, NoReturn

from whisper.worker import Worker
from whisper.packet import Packet
from whisper.packet.v1 import PacketType



class PacketReader(Worker):
    """Reads packet into queue."""


    async def work(self,
        queue: asyncio.Queue[Packet],
        reader: Callable[[], Awaitable[Packet]],
    ) -> NoReturn:
        while True:
            packet = await reader()
            await queue.put(packet)


class PacketWriter(Worker):
    """Writes packet from queue."""

    async def work(self,
        queue: asyncio.Queue[Packet],
    writer: Callable[[Packet], Awaitable[None]],
    ) -> NoReturn:
        while True:
            packet = await queue.get()
            await writer(packet)


class ResponseHandler(Worker):
    """Invokes respective handler for packet."""

    async def work(self,
        queue: asyncio.Queue[Packet],
        handler: Callable[[PacketType], Callable[[bytes], None]],
    ) -> NoReturn:
        while True:
            packet = await queue.get()
            handle = handler(packet.kind) # type: ignore
            handle(packet.data)
