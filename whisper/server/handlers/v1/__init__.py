"""
This module provides request packet-v1 handlers.
"""

from typing import Tuple, Type

from .base import RequestV1Handler
from .init_handler import InitV1Handler
from .exit_handler import ExitV1Handler


__all__ = (
    "RequestV1Handler",
    "InitV1Handler",
    "ExitV1Handler",
    "Handlers",
)

Handlers: Tuple[Type[RequestV1Handler], ...] = (
    InitV1Handler,
    ExitV1Handler,
)
