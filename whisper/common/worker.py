"""
This module provides worker object.
"""

import abc
import asyncio

from whisper.logger import Logger


class Worker(abc.ABC):
    """Abstract base class for worker object."""

    def __init__(self, logger: Logger):
        self.name = type(self).__name__
        self.logger = logger

    async def __call__(self, *args, **kwargs):
        try:
            await self.work(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as ex:
            self.logger.exception(str(ex))
        finally:
            self.logger.info(f"{self.name} finished")

    @abc.abstractmethod
    async def work(self, *args, **kwargs):
        """Worker task."""
