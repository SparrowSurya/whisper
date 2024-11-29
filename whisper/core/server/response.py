from dataclasses import dataclass
from typing import Iterable

from whisper.core.packet import Packet
from .handle import ConnHandle


@dataclass(frozen=True, repr=False, slots=True)
class Response:
    """A response packet for multiple recipients."""

    packet: Packet
    """Response packet."""

    receivers: Iterable[ConnHandle]
    """Response receivers."""

    def __repr__(self) -> str:
        return f"<Response: {self.packet!r} to {self.receivers!s}>"
