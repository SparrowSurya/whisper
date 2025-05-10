"""
This module provides init packet-v1 response handler.
"""

from whisper.packet.v1 import PacketType
from whisper.packet.v1.exit_packet import ExitReason
from .base import PacketV1ResponseHandler


class ExitHandler(PacketV1ResponseHandler):
    """Handles init packet response handler."""

    @staticmethod
    def packet_type():
        return PacketType.EXIT

    def handle(self, reason: ExitReason, *args, **kwargs):
        pass
