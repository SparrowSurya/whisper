"""
This package contains request packet handler classes for server.
"""

from typing import List, Type

from .base import RequestPacketHandler # noqa: F401
from .init_handler import InitHandler # noqa: F401
from .exit_handler import ExitHandler # noqa: F401


handlers: List[Type[RequestPacketHandler]] = [
    InitHandler,
    ExitHandler,
]
