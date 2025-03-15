"""
This module contains the mechanism for communicating and action on the
response sent by the server.
"""

import abc
import asyncio
from concurrent.futures import Future, InvalidStateError
from typing import Coroutine, List, Set, Any


class EventLoop(abc.ABC):
    """
    The class provides the asynchronous eventloop using `asyncio`. It
    provides mthods to control the running eventloop.
    """

    def __init__(self):
        self._stop_fut = Future()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Running eventloop."""
        return asyncio.get_running_loop()

    def schedule(self, coro: Coroutine[Any, Any, Any]) -> Future[Any]:
        """Schedules a coroutine (threadsafe) into event loop."""
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def create_task(self,
        task: Coroutine[Any, Any, Any],
    ) -> asyncio.Task[Any]:
        """Provides a task (not threadsafe) object."""
        return asyncio.create_task(task)

    async def keep_running(self):
        """This keeps the eventloop running until it is stopped."""
        await asyncio.wrap_future(self._stop_fut)

    def stop_running(self):
        """Stops the running execution of running tasks in eventloop."""
        try:
            self._stop_fut.set_result(None)
        except InvalidStateError:
            pass

    async def process_tasks(self
    ) -> List[Future[Coroutine[Any, Any, Any] | BaseException]]:
        """Process the coroutines and tasks."""
        running_tasks = [self.create_task(task) for task in self.get_tasks()]
        await self.keep_running()
        for task in running_tasks:
            task.cancel()
        return await asyncio.gather(*running_tasks, return_exceptions=True)

    @abc.abstractmethod
    def get_tasks(self) -> Set[Coroutine[Any, Any, Any]]:
        """Provides the set of tasks to start with."""
