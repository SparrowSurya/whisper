"""
This module provides a response object for sending packet to multiple
connections.
"""

from dataclasses import dataclass
from typing import Iterable

from whisper.core.packet import Packet
from .handle import ConnHandle


@dataclass(frozen=True, repr=False, slots=True)
class Response:
    """A response packet for multiple recipients."""

    packet: Packet
    receivers: Iterable[ConnHandle]
