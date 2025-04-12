"""
This module provides init packet response handler.
"""

from whisper.packet.v1 import PacketType
from whisper.packet.v1.exit_packet import ExitReason
from .base import ResponsePacketHandler


class ExitHandler(ResponsePacketHandler):
    """Handles init packet response handler."""

    @classmethod
    def packet_type(cls):
        return PacketType.EXIT

    def handle(self, reason: ExitReason, *args, **kwargs):
        pass
