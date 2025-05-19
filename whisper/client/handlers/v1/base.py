"""
This module provides base packet-v1 abstract handler class.
"""

import abc
import logging
from typing import Any

from whisper.packet.v1 import PacketV1, Status, PacketType
from whisper.client.handlers.base import AbstractResponseHandler


logger = logging.getLogger(__name__)


class ResponseV1Handler(AbstractResponseHandler[PacketV1, PacketType]):
    """Handles response for packet-v1."""

    @staticmethod
    def version() -> int:
        """Provide the packet version it handles."""
        return PacketV1.version()

    @abc.abstractmethod
    def handle(self, status: Status, **kwargs: Any):
        """Handle the response."""

    def validate_packet(self, packet: PacketV1):
        if packet.version() != self.version():
            msg = (
                f"wrong packet version: expected {self.version()}, "
                f"got {packet.version()}")
            logger.errror(msg)
            raise ValueError(msg)

        if self.unique_key() != packet.type:
            msg = (
                f"wrong packet type: expected {self.unique_key()}, "
                f"got {packet.type}")
            logger.errror(msg)
            raise ValueError(msg)
