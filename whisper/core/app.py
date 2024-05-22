from __future__ import annotations
import asyncio
import concurrent.futures
from argparse import ArgumentParser
from typing import Sequence, Callable, Coroutine, Any

from .stream import Stream
from .manager import Manager


class BaseApp:
    """Base application (asynchronous backend)."""

    def __init__(self, argv: Sequence[str]):
        self.args = self.parser().parse_args(argv)
        self.loop_fut = concurrent.futures.Future()
        self.stop_fut = concurrent.futures.Future()
        self.exit_fut = concurrent.futures.Future()
        self.queue: asyncio.Queue[bytes] = asyncio.Queue()
        self.stream = Stream()
        self.manager = Manager(self)

    def run(self):
        """Start the event loop."""
        try:
            asyncio.run(self._run_forever())
        finally:
            self.exit_fut.set_result(None)

    async def _run_forever(self):
        """Lifetime of the event loop. All the tasks should be done inside it."""
        self.loop_fut.set_result(asyncio.get_running_loop())
        await self.stream.open(host=self.args.hostip, port=self.args.port, loop=self.loop)
        self.init_tasks()
        await asyncio.wrap_future(self.stop_fut)
        await self.stream.close()

    def stop(self):
        """This closes the event loop."""
        try:
            self.stop_fut.set_result(None)
        except concurrent.futures.InvalidStateError:
            pass

    def create_task(
        self,
        task: Coroutine[Any, Any, None],
        on_done: Callable[[concurrent.futures.Future[None]], None] | None = None,
    ) -> concurrent.futures.Future:
        """Create a task in the event loop.
        `on_done` is called when the task is complete.
        """
        fut = asyncio.run_coroutine_threadsafe(task, self.loop)
        if on_done is not None:
            fut.add_done_callback(on_done)
        return fut

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Running event loop."""
        return self.loop_fut.result()

    def parser(self) -> ArgumentParser:
        """Parser object to parse the arguments to the application."""
        parser = ArgumentParser()

        parser.add_argument("-u", "--user", type=str, required=True, help="username.")
        parser.add_argument(
            "-ip", "--hostip", type=str, required=True, help="ip address of server."
        )
        parser.add_argument(
            "-p", "--port", type=int, required=True, help="port number of the server."
        )

        return parser

    def init_tasks(self):
        """Task that need to run as soon as connection establishes."""