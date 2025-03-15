"""
This module contains the mechanism for communicating and action on the
response sent by the server.
"""

import logging
from typing import Coroutine, Set, Any

from .core.packet import Packet
from .core.client import BaseClient, ClientConn
from .core.eventloop import EventLoop
from .settings import Setting


logger = logging.getLogger(__name__)


class Client(BaseClient, EventLoop):
    """
    The class provides the asynchronous client backend actions for the
    app. It uses `asyncio` event loop to manage async tasks.
    """

    def __init__(self, conn: ClientConn | None = None):
        """The `conn` object is used to connect with remote server."""
        BaseClient.__init__(self, conn)
        EventLoop.__init__(self)
        self.setting = Setting.from_defaults()

    def send_packet(self, packet: Packet):
        """Schedules the packet in the outgoing queue."""
        self.schedule(self.sendq.put(packet))

    async def main(self):
        """
        This defines the entry point of backend. It determines the
        series of events (lifecycle) in backend.
        """
        host, port = self.setting.get("host"), self.setting.get("port")
        self.connect(host, port)
        await self.process_tasks()
        self.disconnect()

    def get_tasks(self) -> Set[Coroutine[Any, Any, Any]]:
        """Provides a set of tasks to start with."""
        return {self.reader(), self.writer()}
