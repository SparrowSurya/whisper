"""
This module provides decorator for backend asyncio workers.
"""

import asyncio
import logging
from typing import Any, Callable, NoReturn, Awaitable


def worker(name: str, logger: logging.Logger):
    """Provide error handelling for worker coroutine method."""
    name = f"Worker-{name}"

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
