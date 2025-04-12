"""
This module provides init packet response handler.
"""

from whisper.packet.v1 import PacketType
from .base import ResponsePacketHandler


class InitHandler(ResponsePacketHandler):
    """Handles init packet response handler."""

    @classmethod
    def packet_type(cls):
        return PacketType.INIT

    def handle(self, username: str, *args, **kwargs):
        pass
