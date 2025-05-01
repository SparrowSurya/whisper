"""
This module provides init packet implementation for packet v1.
"""


from typing import Any, Dict

from whisper.codec import json_decode, json_encode
from .base import PacketType, PacketV1, PacketV1Registery, Status


@PacketV1Registery.register
class InitPacket(PacketV1):

    @staticmethod
    def packet_type() -> PacketType:
        return PacketType.INIT

    @classmethod
    def request(cls, *, username: str, **kwargs):
        content = { "username": username, **kwargs}
        return cls.create(json_encode(content))

    @classmethod
    def response(cls, *, status: Status, **kwargs):
        return cls.create(json_encode(kwargs), status)

    def content(self) -> Dict[str, Any]:
        return json_decode(self.data)
