"""
This module provides exit packet request handler.
"""

from whisper.packet.v1 import PacketType, ExitReason
from whisper.server.connection import ConnHandle
from .base import RequestPacketHandler


class ExitHandler(RequestPacketHandler):
    """Handles exit packet request."""

    @classmethod
    def packet_type(cls):
        return PacketType.EXIT

    def handle(self,
        conn: ConnHandle,
        *args,
        reason: ExitReason = ExitReason.UNKNOWN,
        **kwargs,
    ):
        """Read reason and provide response."""
        conn.close = True
