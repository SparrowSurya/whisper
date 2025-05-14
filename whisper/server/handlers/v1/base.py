"""
This module provide base response packet-v1 abstract handler class.
"""

import abc
import logging

from whisper.server.handlers.base import AbstractRequestHandler
from whisper.packet.v1 import PacketV1, PacketType


logger = logging.getLogger(__name__)

class RequestV1Handler(AbstractRequestHandler[PacketV1]):
    """Common packet handler base class for packet-v1."""

    @staticmethod
    @abc.abstractmethod
    def packet_type() -> PacketType:
        """This defines the packet type implemented by this packet."""
        raise NotImplementedError

    def validate_packet(self, packet: PacketV1):
        """Validates the appropriate packet version."""
        if self.packet_type() != packet.type:
            msg = (
                f"incorrect packet-v1 type: expected {self.packet_type()}, got "
                f"{packet.type}")
            logger.error(msg)
            raise ValueError(msg)
