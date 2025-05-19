"""
This module provides exit packet-v1 response handler.
"""

from whisper.packet.v1 import PacketType, Status
from whisper.packet.v1.exit_packet import ExitReason, ExitV1Packet
from .base import ResponseV1Handler


class ExitV1Handler(ResponseV1Handler):
    """Exit packet-v1 handler implementation."""

    @staticmethod
    def unique_key() -> PacketType:
        return ExitV1Packet.unique_key()

    def handle(self, status: Status, reason: ExitReason, *args, **kwargs):
        pass
