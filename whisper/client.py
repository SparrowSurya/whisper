"""
This module contains the mechanism for communicating and action on the
response sent by the server.
"""

import asyncio
import logging
from concurrent.futures import Future, InvalidStateError
from typing import Coroutine, Set, Any

from .core.packet import Packet
from .core.client import BaseClient, ClientConn
from .settings import Setting


logger = logging.getLogger(__name__)


class Client(BaseClient):
    """
    The class provides the asynchronous client backend actions for the
    app. It uses `asyncio` the event loop to manage async tasks.
    """

    def __init__(self, conn: ClientConn | None = None):
        """The `conn` object is used to connect with remote server."""
        BaseClient.__init__(self, conn)
        self.setting = Setting.from_defaults()
        self.stop_fut: Future[None] = Future()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Asyncio running eventloop."""
        return asyncio.get_running_loop()

    def schedule(self, task: Coroutine[Any, Any, Any]) -> Future[Any]:
        """Schedules a task (threadsafe) into event loop."""
        return asyncio.run_coroutine_threadsafe(task, self.loop)

    def send_packet(self, packet: Packet) -> Future[Any]:
        """Schedules the packet in the queue."""
        return self.schedule(self.sendq.put(packet))

    async def main(self):
        """
        This defines the entry point of backend. It determines the
        series of events (lifecycle) in backend.
        """
        host, port = self.setting.get("host"), self.setting.get("port")
        self.connect(host, port)
        await self.process_tasks()
        self.disconnect()

    def stop(self):
        """Sets the `stop_fut` result to signal for `process_tasks` ending."""
        try:
            self.stop_fut.set_result(None)
        except InvalidStateError:
            pass

    async def process_tasks(self):
        """Coroutine handelling the various events."""
        running_tasks = [asyncio.create_task(task) for task in self.get_tasks()]

        # Wait for the stop_fut to complete
        await asyncio.wrap_future(self.stop_fut)

        for task in running_tasks:
            task.cancel()

        return await asyncio.gather(*running_tasks, return_exceptions=True)

    def get_tasks(self) -> Set[Coroutine[Any, Any, Any]]:
        """Provides a set of tasks to start with."""
        return {self.reader(), self.writer()}
