"""
This module provide base response handler for client.
"""

from typing import Any, TypeVar

from whisper.packet import Packet
from whisper.handler import AbstractPacketHandler


_P = TypeVar("_P", bound=Packet)
_K = TypeVar("_K", bound=Any)

class AbstractResponseHandler(AbstractPacketHandler[_P, _K, Any]):
    """
    Response packet handler for client. It handles response packet from server and
    performs required actions on client side.
    """

    def __call__(self, packet: _P, /, *args): # type: ignore[override]
        return super().__call__(packet, packet.status, *args)
