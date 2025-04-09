"""
This module provides `ExitPacket` class.
"""

import struct
from enum import IntEnum, auto
from typing import Awaitable, Callable

from .base import PacketType, PacketV1, PacketV1Registery


class ExitReason(IntEnum):

    SELF_EXIT = auto()
    FORCE_EXIT = auto()


@PacketV1Registery.register
class ExitPacket(PacketV1):

    @classmethod
    def packet_type(cls) -> PacketType:
        return PacketType.EXIT

    @classmethod
    def create(cls, reason: str):
        return cls(
            type_=cls.packet_type(),
            data=reason.encode(encoding="utf-8"),
        )

    @classmethod
    async def from_stream(cls,
        reader: Callable[[int], Awaitable[bytes]],
    ):
        length = struct.unpack("H", await reader(2))[0]
        data = await reader(length)
        return cls(cls.packet_type(), data)

    def content(self) -> str:
        """Provide the exit reason message."""
        return self.data.decode(encoding="UTF-8")
