"""
This module provides packet-v1 response handlers.
"""

from typing import Tuple, Type

from .base import ResponseV1Handler
from .init_handler import InitV1Handler
from .exit_handler import ExitV1Handler


__all__ = (
    "ResponseV1Handler",
    "InitV1Handler",
    "ExitV1Handler",
    "Handlers",
)

Handlers: Tuple[Type[ResponseV1Handler], ...] = (
    InitV1Handler,
    ExitV1Handler,
)
