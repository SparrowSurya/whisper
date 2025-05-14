"""
This package provides request packet handler classes for server.
"""

from typing import Tuple, Dict, Type

from .base import AbstractRequestHandler
from .v1 import Handlers as V1Handlers


__all__ = (
    "AbstractRequestHandler",
    "Handlers",
)

Handlers: Dict[int, Tuple[Type[AbstractRequestHandler], ...]] = {
    1: V1Handlers,
}
