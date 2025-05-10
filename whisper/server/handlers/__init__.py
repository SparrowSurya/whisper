"""
This package contains request packet handler classes for server.
"""

from typing import List, Type

from .base import PacketV1RequestHandler
from .init_handler import InitHandler
from .exit_handler import ExitHandler


__all__ = (
    "PacketV1RequestHandler",
    "InitHandler",
    "ExitHandler",
    "handlers",
)

handlers: List[Type[PacketV1RequestHandler]] = [
    InitHandler,
    ExitHandler,
]
