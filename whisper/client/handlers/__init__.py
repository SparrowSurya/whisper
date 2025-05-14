"""
This package provides response packet handlers for client.
"""

from typing import Tuple, Dict, Type

from .base import AbstractResponseHandler
from .v1 import Handlers as V1Handlers


__all__ = (
    "AbstractResponseHandler",
    "Handlers",
)

Handlers: Dict[int, Tuple[Type[AbstractResponseHandler], ...]] = {
    1: V1Handlers,
}
