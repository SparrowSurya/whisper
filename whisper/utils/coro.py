"""
This module provides utility for coroutines.
"""

import asyncio
import logging
from typing import Any, Callable, NoReturn, Awaitable


logger = logging.getLogger(__name__)


def handle_cancellation(name: str):
    """Provide error handelling for coroutines."""

    def wrapper(func: Callable[[], Awaitable[NoReturn]]):
        async def inner(*args: Any, **kwargs: Any):
            try:
                logger.debug(f"{name} running")
                await func(*args, **kwargs) # type: ignore
            except asyncio.CancelledError:
                pass
            except Exception:
                logger.exception(f"{name} got execption")
            finally:
                logger.debug(f"{name} finished")

        return inner
    return wrapper
