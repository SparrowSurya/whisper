"""
This module contains the mechanism for communicating and action on the response sent
by the server.
"""

import asyncio
from concurrent.futures import Future
from typing import Coroutine, List, Dict, Set, Any


class EventLoop:
    """The class provides the asynchronous eventloop using `asyncio`. It provides
    methods to control the running eventloop.

    **Attributes & Properties**:
    * loop - asyncio eventloop

    **Methods**:
    * run_coro - run coroutine
    * exectue - executes the eventloop unill stopped
    * schedule - schedule a task from another thread
    * create_task - create a task (must be called from same thread)
    * stop_eventloop - stop the eventloop
    * initial_tasks - any task that need to run as soon as eventloop starts
    * exception_handler - handle exception in asyncio tasks
    """

    def __init__(self):
        self._stop_event = asyncio.Event()
        self._loop = asyncio.get_event_loop()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Eventloop instance."""
        return self._loop

    def run_coro(self, coro: Coroutine[None, None, Any]) -> BaseException | None:
        """Run given coroutine in eventloop. It returns exceptions caught during
        execution if any."""
        error = None
        asyncio.set_event_loop(self.loop)
        self.loop.set_exception_handler(self.exception_handler)
        self._stop_event.clear()
        try:
            asyncio.run(coro)
        except BaseException as ex:
            error = ex
        return error

    async def execute(self) -> List[Future[Coroutine[Any, Any, Any] | BaseException]]:
        """This executes tasks and blocks the thread until stopped."""
        running_tasks = [self.create_task(task) for task in self.initial_tasks()]
        await self._stop_event.wait()
        for task in running_tasks:
            task.cancel()
        return await asyncio.gather(*running_tasks, return_exceptions=True)

    def schedule(self, coro: Coroutine[Any, Any, Any]) -> Future[Any]:
        """Runs coroutine from other threads.."""
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def create_task(self,
        coro: Coroutine[Any, Any, Any],
        name: str | None = None,
    ) -> asyncio.Task[Any]:
        """Run coroutine in eventloop. Must be called from same thread."""
        return self.loop.create_task(coro, name=name)

    def stop_eventloop(self):
        """This signals the eventloop to close."""
        self._stop_event.set()

    def initial_tasks(self) -> Set[Coroutine[Any, Any, Any]]:
        """Provides a set of initial tasks."""
        return set()

    def exception_handler(self,
        loop: asyncio.AbstractEventLoop,
        context: Dict[str, Any],
    ):
        """Handle exception in running task."""
