"""
This module provides exit packet-v1 request handler.
"""

from whisper.packet.v1 import PacketType, ExitReason, ExitV1Packet
from whisper.server.connection import ConnHandle
from .base import RequestV1Handler


class ExitV1Handler(RequestV1Handler):

    @staticmethod
    def packet_type() -> PacketType:
        return PacketType.EXIT

    @staticmethod
    def unique_key():
        return ExitV1Packet.unique_key()

    def handle(self,
        conn: ConnHandle,
        *args,
        reason: ExitReason | None = None,
        **kwargs,
    ):
        conn.close = True
