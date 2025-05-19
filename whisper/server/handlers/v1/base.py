"""
This module provide base response packet-v1 abstract handler class.
"""

import logging

from whisper.server.handlers.base import AbstractRequestHandler
from whisper.packet.v1 import PacketV1, PacketType


logger = logging.getLogger(__name__)

class RequestV1Handler(AbstractRequestHandler[PacketV1, PacketType]):
    """Common packet handler base class for packet-v1."""

    def validate_packet(self, packet: PacketV1):
        """Validates the appropriate packet version."""
        if self.unique_key() != packet.type:
            msg = (
                f"incorrect packet-v1 type: expected {self.unique_key()}, got "
                f"{packet.type}")
            logger.error(msg)
            raise ValueError(msg)
