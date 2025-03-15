"""
This module provides handler workers for connections.
"""

from asyncio import Queue, AbstractEventLoop, get_running_loop
from typing import Any, Callable, Awaitable, Dict

from whisper.utils.decorators import handle_cancellation
from .packet import Packet, PacketKind
from .codec import deserialize


class PacketReader:
    """Reads incoming packet from connection reader."""

    def __init__(self,
        queue: Queue[Packet],
        reader: Callable[[int, AbstractEventLoop], Awaitable[bytes]],
    ):
        self.queue = queue
        self.reader = reader

    @handle_cancellation("PacketReader")
    async def __call__(self):
        loop = get_running_loop()
        reader = lambda n: self.reader(n, loop)  # noqa: E731

        while True:
            packet = await Packet.from_stream(reader)
            await self.queue.put(packet)

    def __repr__(self):
        return f"<cls: {self.__class__.__name__}>"


class PacketWriter:
    """Writes outgoing packets to connection writer."""

    def __init__(self,
        queue: Queue[Packet],
        writer: Callable[[bytes, AbstractEventLoop], Awaitable[None]],
    ):
        self.queue = queue
        self.writer = writer

    @handle_cancellation("PacketWriter")
    async def __call__(self):
        loop = get_running_loop()
        writer = lambda d: self.writer(d, loop)  # noqa: E731

        while True:
            packet = await self.queue.get()
            data = packet.to_stream()
            await writer(data)

    def __repr__(self):
        return f"<cls: {self.__class__.__name__}>"


class PacketHandler:
    """Handles the received packet."""

    def __init__(self,
        queue: Queue[Packet],
        handlers: Dict[PacketKind, Callable[[Dict[str, Any]], None]],
    ):
        self.queue = queue
        self.handlers = handlers

    @handle_cancellation("PacketHandler")
    async def __call__(self):
        while True:
            packet = await self.queue.get()
            data = deserialize(packet.data)
            handle = self.handlers[packet.kind]
            handle(**data)

    def __repr__(self):
        return f"<cls: {self.__class__.__name__}>"
