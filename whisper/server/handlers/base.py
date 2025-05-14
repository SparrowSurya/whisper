"""
This module provides abstract base request packet handler class for server.
"""

from typing import Any, TypeVar

from whisper.server.connection import ConnHandle
from whisper.handler import AbstractPacketHandler
from whisper.packet import Packet


_P = TypeVar("_P", bound=Packet)

class AbstractRequestHandler(AbstractPacketHandler[_P, Any]):
    """Base packet handler class for server handlers."""

    def __call__(self, packet: _P, conn: ConnHandle, /, *args): # type: ignore[override]
        return super().__call__(packet, conn, *args)

    @staticmethod
    def unique_key() -> Any:
        """Provide the unique key same as the packet handeled."""
