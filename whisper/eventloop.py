"""
This module contains the eventloop to manage the running tasks and coroutines with
graceful exit.
"""

import sys
import signal
import asyncio
import threading
from concurrent.futures import Future
from typing import Tuple, List, Dict, Set, Any, Callable, Coroutine, ParamSpec, TypeVar


T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")

class EventLoop:
    """
    The class provides the asynchronous eventloop using `asyncio`. It handles
    exceptions and signals for graceful exit.

    **Attributes & Properties**:
    * loop - asyncio eventloop
    * signals - signals that will be handled by the eventloop
    * CancelledError - error raised when coroutine is cancelled

    **Methods**:
    * run_main - run coroutine
    * main - coroutine between setup and teardown
    * schedule - schedule a task from another thread
    * create_task - create a task (must be called from same thread)
    * stop_main - finish the execution of `main` coroutine above
    * signal_handler - handles the received signal to the process
    * exception_handler - handle uncaught exception in eventloop tasks
    * initial_tasks - any task that need to run as soon as eventloop starts
    * stop_main_result - a value that was given while calling `stop_main`
    """

    signals: List[int] = [signal.SIGINT, signal.SIGTERM]
    if sys.platform == "win32":
        signals.extend((signal.SIGBREAK, signal.CTRL_C_EVENT, signal.CTRL_BREAK_EVENT))
    else:
        signals.append(signal.SIGQUIT)

    CancelledError = asyncio.CancelledError

    def __init__(self):
        self._stop_event = Future()
        self._loop = asyncio.get_event_loop()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Eventloop instance."""
        return self._loop

    def run_main(self,
        coro: Callable[P, Coroutine[Any, Any, R]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> BaseException | None:
        """Runs given coroutine in eventloop until finishes. It returns exceptions
        caught during execution if any."""
        asyncio.set_event_loop(self.loop)
        if threading.current_thread() is threading.main_thread():
            for sig in self.signals:
                self.loop.add_signal_handler(sig, lambda: self.signal_handler(sig))
        self.loop.set_exception_handler(self.exception_handler)
        if self._stop_event.done():
            self._stop_event = Future()
        try:
            self.loop.run_until_complete(coro(*args, **kwargs))
        except BaseException as ex:
            return ex
        return None

    async def main(self) -> List[Future[R | BaseException]]:
        """It processes eventloop tasks until stopped."""
        for name, fn in self.initial_tasks():
            self.create_task(fn(), name)
        await asyncio.wrap_future(self._stop_event)
        tasks = [
            task for task in asyncio.all_tasks()
            if task is not asyncio.current_task()
        ]
        for task in tasks:
            task.cancel()
        return await asyncio.gather(*tasks, return_exceptions=True)

    def schedule(self, coro: Coroutine[Any, Any, Any]) -> Future[Any]:
        """Runs coroutine from other threads.."""
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def create_task(self,
        coro: Coroutine[Any, Any, Any],
        name: str | None = None,
    ) -> asyncio.Task[Any]:
        """Run coroutine in eventloop. Must be called from same thread."""
        return self.loop.create_task(coro, name=name)

    def stop_main(self, result: Any = None):
        """This signals the `main` coroutine to finish."""
        if not self._stop_event.done():
            self._stop_event.set_result(result)

    def signal_handler(self, sig: int | None = None):
        """Handle the received signal."""
        self.stop_main()

    def exception_handler(self,
        loop: asyncio.AbstractEventLoop,
        context: Dict[str, Any],
    ):
        """Handle exception in running task."""
        self.stop_main()

    def initial_tasks(self) -> Set[Tuple[str | None, Callable[[], Coroutine[Any, Any, None]]]]:
        """Provides a set of initial tasks."""
        return set()

    def stop_main_result(self) -> T:
        """Provides the value given to `stop_main`."""
        return self._stop_event.result()
