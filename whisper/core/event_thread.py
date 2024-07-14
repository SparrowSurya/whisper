import asyncio
import concurrent.futures
from typing import Callable, Coroutine, Any


# Source Refrence - https://gist.github.com/thegamecracks/564bd55af973827f8a05b48f197d5c09
class EventThread:
    """
    It provieds mechansim for backend asynchronous tasks to run in seperate thread.
    The class should be inherited by child and provide the suitable definitions.

    It also allows integration with frontend, while ui runs in main thread.

    Methods:
    * `init_main` - performs setup tasks.
    * `init_coro` - initialize tasks.
    * `exit_main` - performs cleanup tasks.
    * `stop` - stop running tasks.
    * `schedule` - schedule task in event loop.
    * `main` - main entry point for coroutine execution.
    * `start` - function to run in seperate thread.
    * `on_finish` - invoke callback after `main()` finishes.
    """

    def __init__(self):
        self.loop_fut = concurrent.futures.Future()
        self.stop_fut = concurrent.futures.Future()
        self.exit_fut = concurrent.futures.Future()

    def start(self):
        """
        This starts the execution of coroutines in asyncio event loop.
        It can also be run in seperate thread.
        """
        try:
            asyncio.run(self.main())
        finally:
            self.exit_fut.set_result(None)

    async def main(self):
        """
        The main entry point for coroutines execution.
        This is used by `start` method to execute coroutines.
        """
        self.loop_fut.set_result(asyncio.get_running_loop())
        await self.init_main()
        self.init_coro()
        await asyncio.wrap_future(self.stop_fut)  # blocks until stop() is called
        await self.exit_main()

    def stop(self):
        """Stops the scheduled/running tasks."""
        try:
            self.stop_fut.set_result(None)
        except concurrent.futures.InvalidStateError:
            pass

    def schedule(
        self,
        task: Coroutine[Any, Any, None],
        on_done: Callable[[concurrent.futures.Future[None]], None] | None = None,
    ) -> concurrent.futures.Future:
        """
        Schedules a task.
        `on_done` is called when the task is complete.
        """
        fut = asyncio.run_coroutine_threadsafe(task, self.loop)
        if on_done is not None:
            fut.add_done_callback(on_done)
        return fut

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Asyncio running eventloop."""
        return self.loop_fut.result()

    def on_finish(
        self,
        callback: Callable[[concurrent.futures.Future[None]], None],
    ):
        """Callback after the `main()` finished execution."""
        self.exit_fut.add_done_callback(callback)

    async def init_main(self):
        """
        Coroutines needed to run as event loop starts.
        Use this for initilization or setup purposes.
        """

    def init_coro(self):
        """Schedule coroutines needed to run after the `init_main()` method has been executed."""

    async def exit_main(self):
        """
        Coroutines that needs to run after `stop()` method has been called.
        Use this to cleanup purposes.
        """
