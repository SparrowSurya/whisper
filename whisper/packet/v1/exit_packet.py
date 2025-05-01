"""
This module provides exit packet implementation for packet v1.
"""

import struct
from enum import IntEnum, auto

from .base import PacketType, PacketV1, PacketV1Registery, Status


class ExitReason(IntEnum):
    """Describe the exit reason for client and server."""

    UNKNOWN = auto()
    EXCEPTION = auto()
    SELF_EXIT = auto()
    FORCE_EXIT = auto()


@PacketV1Registery.register
class ExitPacket(PacketV1):

    @staticmethod
    def packet_type() -> PacketType:
        return PacketType.EXIT

    @classmethod
    def request(cls, reason: ExitReason):
        value = (reason & 0x0F) << 4
        return cls.create(struct.pack("B", value))

    @classmethod
    def response(cls, reason: ExitReason, status: Status):
        data = struct.pack("B", (reason & 0x0F) << 4)
        return cls.create(data, status)

    def content(self) -> ExitReason:
        value = struct.unpack("B", self.data)[0] >> 4
        return ExitReason(value)
