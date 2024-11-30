import asyncio
import logging
from typing import Any, Callable, NoReturn, Awaitable


def aworker(name: str, logger: logging.Logger):
    """Provide error handelling for worker coroutine method."""
    worker = f"Worker-{name}"

    # def wrapper(func: Coroutine[Any, Any, NoReturn]):
    def wrapper(func: Callable[[], Awaitable[NoReturn]]):
        async def inner(*args: Any, **kwargs: Any):
            try:
                logger.debug(f"{worker} running")
                await func(*args, **kwargs) # type: ignore
            except asyncio.CancelledError:
                pass
            except Exception:
                logger.exception(f"{worker} got execption")
            finally:
                logger.debug(f"{worker} finished")

        return inner
    return wrapper
