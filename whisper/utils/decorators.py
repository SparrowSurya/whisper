import asyncio
import logging
from typing import Any, Coroutine


def aworker(name: str, logger: logging.Logger):
    """Provide error handelling for worker coroutine method."""
    worker = f"Worker-{name}"

    def wrapper(func: Coroutine[Any, Any, None]):
        async def inner(*args, **kwargs):
            try:
                logger.debug(f"{worker} running")
                await func(*args, **kwargs)
            except asyncio.CancelledError:
                pass
            except Exception:
                logger.exception(f"{worker} got execption")
            finally:
                logger.debug(f"{worker} finished")

        return inner
    return wrapper
