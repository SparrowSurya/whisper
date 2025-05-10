"""
This module provides init packet-v1 response handler.
"""

from whisper.packet.v1 import PacketType
from .base import PacketV1ResponseHandler


class InitHandler(PacketV1ResponseHandler):
    """Handles init packet response handler."""

    @staticmethod
    def packet_type():
        return PacketType.INIT

    def handle(self, username: str, *args, **kwargs):
        pass
