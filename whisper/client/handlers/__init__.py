"""
This package provides response packet-v1 handler for client.
"""

from typing import List, Type

from .base import PacketV1ResponseHandler
from .init_handler import InitHandler
from .exit_handler import ExitHandler


__all__ = (
    "PacketV1ResponseHandler",
    "InitHandler",
    "ExitHandler",
    "handlers",
)


handlers: List[Type[PacketV1ResponseHandler]] = [
    InitHandler,
    ExitHandler,
]
