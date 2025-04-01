"""
This module provides `InitPacket` implementation for `PacketV1`.
"""


import struct
from typing import Any, Dict, Awaitable, Callable

from whisper.core.codec import json_decode, json_encode
from .base import PacketType, PacketV1, PacketV1Registery


@PacketV1Registery.register
class InitPacket(PacketV1):

    @classmethod
    def packet_type(cls) -> PacketType:
        return PacketType.INIT

    @classmethod
    def create(cls, username: str):
        content = { "username": username }
        return cls(
            type_=cls.packet_type(),
            data=json_encode(content),
        )

    @classmethod
    async def from_stream(cls,
        reader: Callable[[int], Awaitable[bytes]],
    ):
        length = struct.unpack("H", await reader(2))[0]
        data = await reader(length)
        return cls(cls.packet_type(), data)

    def content(self) -> Dict[str, Any]:
        return json_decode(self.data)
