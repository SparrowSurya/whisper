"""
This module provides handler workers for connections.
"""


from asyncio import Queue, AbstractEventLoop, get_running_loop
from dataclasses import dataclass
import logging
from typing import Callable, Awaitable

from whisper.utils.decorators import worker
from .packet import Packet


logger = logging.getLogger(__name__)


@dataclass(frozen=True, repr=False)
class PacketReader:
    """Reads incoming packet from connection reader."""

    queue: Queue[Packet]
    reader: Callable[[int, AbstractEventLoop], Awaitable[bytes]]
    should_read: Callable[[], Awaitable[bool]]

    @worker("PacketReader", logger=logger)
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

    @worker("PacketWriter", logger=logger)
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
