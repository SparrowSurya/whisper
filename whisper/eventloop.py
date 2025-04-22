"""
This module contains the mechanism for communicating and action on the response sent
by the server.
"""

import asyncio
from concurrent.futures import Future, InvalidStateError
from typing import Coroutine, List, Dict, Set, Any


class EventLoop:
    """The class provides the asynchronous eventloop using `asyncio`. It provides
    methods to control the running eventloop."""

    def __init__(self):
        self._stop_fut = Future()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Running eventloop."""
        return asyncio.get_running_loop()

    def schedule(self, coro: Coroutine[Any, Any, Any]) -> Future[Any]:
        """Schedules a coroutine (threadsafe) into event loop."""
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def create_task(self, task: Coroutine[Any, Any, Any]) -> asyncio.Task[Any]:
        """Provides a task (not threadsafe) object."""
        return asyncio.create_task(task)

    async def keep_running(self):
        """This blocks the thread and waits for special task to finish."""
        await asyncio.wrap_future(self._stop_fut)

    def stop_running(self) -> bool:
        """This unblocks the thread by setting result of special task."""
        try:
            self._stop_fut.set_result(None)
        except InvalidStateError:
            pass
        return self._stop_fut.done()

    async def execute(self) -> List[Future[Coroutine[Any, Any, Any] | BaseException]]:
        """This executes tasks and blocks the thread until stopped explicitly."""
        running_tasks = [self.create_task(task) for task in self.initial_tasks()]
        await self.keep_running()
        for task in running_tasks:
            task.cancel()
        return await asyncio.gather(*running_tasks, return_exceptions=True)

    def initial_tasks(self) -> Set[Coroutine[Any, Any, Any]]:
        """Provides a set of initial tasks."""
        return set()

    def set_exception_handler(self):
        """Sets custom exception handler to event loop."""
        self.loop.set_exception_handler(self.set_exception_handler)

    def exception_handler(self,
        loop: asyncio.AbstractEventLoop,
        context: Dict[str, Any],
    ):
        """Handle exception in eventloop."""
