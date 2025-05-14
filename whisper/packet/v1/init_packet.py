"""
This module provides init packet-v1 implementation.
"""


from typing import Any, Dict

from whisper.codec import json_decode, json_encode
from whisper.packet import PacketRegistery
from .base import PacketType, PacketV1, Status


@PacketRegistery.register_handler
class InitV1Packet(PacketV1):

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

    def contents(self) -> Dict[str, Any]:
        return json_decode(self.data)
