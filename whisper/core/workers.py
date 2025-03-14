"""
This module provides handler workers for connections.
"""


import logging
from dataclasses import dataclass
from asyncio import Queue, AbstractEventLoop, get_running_loop
from typing import Any, Callable, Awaitable, Dict

from whisper.utils.decorators import handle_cancellation
from .packet import Packet, PacketKind
from .codec import deserialize


logger = logging.getLogger(__name__)


@dataclass(frozen=True, repr=False)
class PacketReader:
    """Reads incoming packet from connection reader."""

    queue: Queue[Packet]
    reader: Callable[[int, AbstractEventLoop], Awaitable[bytes]]
    should_read: Callable[[], Awaitable[bool]]

    @handle_cancellation("PacketReader", logger=logger)
    async def __call__(self):
        """Coroutine reading the packets."""
        loop = get_running_loop()
        reader = lambda n: self.reader(n, loop)  # noqa: E731

        while await self.should_read():
            packet = await Packet.from_stream(reader)
            await self.queue.put(packet)

    def __repr__(self):
        return f"<cls: {self.__class__.__name__}>"


@dataclass(frozen=True, repr=False)
class PacketWriter:
    """Writes outgoing packets to connection writer."""

    queue: Queue[Packet]
    writer: Callable[[bytes, AbstractEventLoop], Awaitable[None]]
    should_write: Callable[[], Awaitable[bool]]

    @handle_cancellation("PacketWriter", logger=logger)
    async def __call__(self):
        """Coroutine writing the packets."""
        loop = get_running_loop()
        writer = lambda d: self.writer(d, loop)  # noqa: E731

        while await self.should_write():
            packet = await self.queue.get()
            data = packet.to_stream()
            await writer(data)

    def __repr__(self):
        return f"<cls: {self.__class__.__name__}>"


@dataclass(frozen=True, repr=False)
class PacketHandler:
    """Handles the received packet."""

    queue: Queue[Packet]
    handlers: Dict[PacketKind, Callable[[Dict[str, Any]], None]]

    @handle_cancellation("PacketHandler", logger=logger)
    async def __call__(self, *args, **kwds):
        """Coroutine handelling the packets."""
        while True:
            packet = await self.queue.get()
            data = deserialize(packet.data)
            handle = self.handlers[packet.kind]
            handle(**data)
