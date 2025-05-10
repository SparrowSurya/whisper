"""
This module provides exit packet-v1 request handler.
"""

from whisper.packet.v1 import PacketType, ExitReason
from whisper.server.connection import ConnHandle
from .base import PacketV1RequestHandler


class ExitHandler(PacketV1RequestHandler):
    """Handles exit packet request."""

    @staticmethod
    def packet_type():
        return PacketType.EXIT

    def handle(self,
        conn: ConnHandle,
        *args,
        reason: ExitReason | None = None,
        **kwargs,
    ):
        """Read reason and provide response."""
        conn.close = True
