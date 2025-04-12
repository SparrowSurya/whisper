"""
This module provides exit packet implementation for packet v1.
"""

import struct
from enum import IntEnum, auto

from .base import PacketType, PacketV1


class ExitReason(IntEnum):
    """Describe the exit reason for client and server."""

    SELF_EXIT = auto()
    FORCE_EXIT = auto()


class ExitPacket(PacketV1):

    @classmethod
    def packet_type(cls) -> PacketType:
        return PacketType.EXIT

    @classmethod
    def request(cls, reason: ExitReason):
        reason = (reason & 0x0F) << 4
        return cls.create(struct.pack("B", reason))

    @classmethod
    def response(cls, reason: ExitReason, code: int):
        reason = (reason & 0x0F) << 4
        return cls.create(struct.pack("B", reason), code)

    def content(self) -> str:
        return self.data.decode(encoding="UTF-8")
