"""
This module provides base packet-v1 abstract handler class.
"""

import abc
import logging
from typing import TypeVar, Any

from whisper.packet.v1 import PacketV1, Status, PacketType
from whisper.client.handlers.base import AbstractPacketHandler


logger = logging.getLogger(__name__)

_P = TypeVar("_P", bound=PacketV1)

class ResponseV1Handler(AbstractPacketHandler[PacketV1]):
    """Handles response for packet-v1."""

    @staticmethod
    def version() -> int:
        """Provide the packet version it handles."""
        return PacketV1.version()

    @abc.abstractmethod
    def handle(self, status: Status, **kwargs: Any):
        """Handle the response."""

    @staticmethod
    @abc.abstractmethod
    def packet_type() -> PacketType:
        """Provide the packet type the handler handles."""

    def validate_packet(self, packet: _P):
        if packet.version() != self.version():
            msg = (
                f"wrong packet version: expected {self.version()}, "
                f"got {packet.version()}")
            logger.errror(msg)
            raise ValueError(msg)

        if self.packet_type() != packet.type:
            msg = (
                f"wrong packet type: expected {self.packet_type()}, "
                f"got {packet.type}")
            logger.errror(msg)
            raise ValueError(msg)
