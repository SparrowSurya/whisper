"""
This module contains the mechanism for communicating and action on the
response sent by the server.
"""

import asyncio
import logging
from concurrent.futures import Future, InvalidStateError
from typing import Coroutine, Dict, Any

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
        self.stop_fut: Future[None] = Future()
        self.setting = Setting.from_defaults()

        # TODO - there must be a better way
        self.tasks: Dict[str, Coroutine[Any, Any, Any]] = {}

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Asyncio running eventloop."""
        return asyncio.get_running_loop()

    def schedule(self, task: Coroutine[Any, Any, Any]) -> Future[Any]:
        """Schedules a task into event loop."""
        return asyncio.run_coroutine_threadsafe(task, self.loop)

    def send_packet(self, packet: Packet) -> Future[Any]:
        """Schedules the packet in the queue."""
        return self.schedule(self.sendq.put(packet))

    async def main(self):
        """
        This defines the entry point of backend. It determines the
        series of events (lifecycle) in backend.
        """
        self.connect(self.setting.get("host"), self.setting.get("port"))
        # TODO - handle workers and tasks and closing
        self.disconnect()

    def stop(self):
        """Stops the scheduled/running tasks."""
        try:
            self.stop_fut.set_result(None)
        except InvalidStateError as error:
            logger.exception(f"Caught exception: {error}")

    def schedule_workers(self):
        """Schedule workers and tasks."""
        self.schedule(self.arecv(lambda n: self.aread(n, self.loop)))
        self.schedule(self.asend(lambda d: self.awrite(d, self.loop)))
        # TODO - packet for connection init
