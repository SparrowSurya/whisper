from __future__ import annotations
import asyncio
import concurrent.futures
from argparse import ArgumentParser
from typing import Sequence, Callable, Coroutine, Any

from .manager import Manager


class BaseApp:
    """Base application (asynchronous backend)."""

    def __init__(self, argv: Sequence[str]):
        self.args = self.parser().parse_args(argv)
        self.loop_fut = concurrent.futures.Future()
        self.stop_fut = concurrent.futures.Future()
        self.exit_fut = concurrent.futures.Future()
        self.queue: asyncio.Queue[bytes] = asyncio.Queue()
        self.manager = Manager(self)
        self.__connected = False

    def run(self):
        """Start the event loop."""
        try:
            asyncio.run(self._run_forever())
        finally:
            self.exit_fut.set_result(None)

    async def _run_forever(self):
        """Lifetime of the event loop. All the tasks should be done inside it."""
        self.loop_fut.set_result(asyncio.get_running_loop())
        await self.connect(host=self.args.hostip, port=self.args.port, loop=self.loop)
        self.init_tasks()
        await asyncio.wrap_future(self.stop_fut)
        await self.disconnect()

    def stop(self):
        """This closes the event loop."""
        try:
            self.stop_fut.set_result(None)
        except concurrent.futures.InvalidStateError:
            pass

    async def connect(
        self, host: str, port: int, loop: asyncio.AbstractEventLoop, **kwargs
    ):
        """
        Open connection with server and initialize the stream objects.

        Arguments:
        * host - host ip address to connect to.
        * port - port number.
        * kwargs - kwargs for `loop.create_connection()`.
        """
        if self.__connected:
            await self.disconnect()

        self.reader = asyncio.StreamReader(limit=2**16, loop=loop)
        self._protocol = asyncio.StreamReaderProtocol(self.reader, loop=loop)
        self.transport, _ = await loop.create_connection(
            lambda: self._protocol, host, port, **kwargs
        )
        self.writer = asyncio.StreamWriter(
            self.transport, self._protocol, self.reader, loop
        )
        self.__connected = True

    async def disconnect(self):
        """Close connection and stream objects."""
        if self.__connected:
            self.__connected = False
            self.writer.close()
            await self.writer.wait_closed()
            del self.writer, self.reader, self._protocol, self.transport

    def init_tasks(self):
        """Task that need to run as soon as connection establishes."""

    async def _read(self, size: int) -> bytes:
        """Read the data received from server."""
        return await self.reader.read(size)

    async def _write(self, data: bytes):
        """Sends the data to server."""
        self.writer.write(data)
        await self.writer.drain()

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
