import json
import asyncio
import logging
from concurrent.futures import Future, InvalidStateError
from typing import Callable, Coroutine, List, Dict, Any, NoReturn

from .core.packet import Packet
from .core.client import BaseClient, ClientConn
from .utils.decorators import aworker
from .settings import Settings


logger = logging.getLogger(__name__)


class Client(BaseClient):
    """
    Client backend controls and manages the connection being used for
    multiple purposes.
    """

    def __init__(self, conn: ClientConn | None = None):
        """
        The connection object is used to connect with remote server.
        Same is used for multiple chats and servers on the client side.
        """
        BaseClient.__init__(self, conn)
        self.stop_fut: Future[None] = Future()
        self.setting = Settings.default()
        self.tasks: List[Future[NoReturn]] = []

    def cfg(self, key: str) -> Any:
        """Get current configuration."""
        return self.setting.get(key)

    def serialize(self, data: Dict[str, Any]) -> bytes:
        """Serialize the dict object into stream of bytes."""
        return json.dumps(data).encode(encoding="UTF-8")

    def deserialize(self, data: bytes) -> Dict[str, Any]:
        """Deserialize the stream of bytes into dict object."""
        return json.loads(data.decode(encoding="UTF-8"))

    def send_packet(self,
        packet: Packet,
        callback: Callable[[Future[None]], None] | None = None,
    ) -> Future[None]:
        """Schedule the packet to be sent to server.
        Callback is invoked after the task finishes."""
        return self.schedule(self.sendq.put(packet), callback)

    @aworker("PacketRecvQueue", logger=logger) # type: ignore
    async def alisten(self) -> NoReturn:
        """Listens the incoming messages to the queue."""
        while True:
            packet = await self.recvq.get()
            self.deserialize(packet.get_data())
            # TODO: what to od with data?

    def stop(self):
        """Stops the scheduled/running tasks."""
        try:
            self.stop_fut.set_result(None)
        except InvalidStateError as error:
            logger.exception(f"Caught exception: {error}")

    def schedule(
        self,
        task: Coroutine[Any, Any, None],
        on_done: Callable[[Future[None]], None] | None = None,
    ) -> Future:
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
        return asyncio.get_running_loop()

    async def main(self):
        """
        The main entry point for coroutines execution.
        This is used by `run` method to execute coroutines.
        """
        self.connect(self.cfg("host"), self.cfg("port"))
        self.schedule_workers()
        await asyncio.wrap_future(self.stop_fut)  # blocks until stop() is called
        self.cancel_workers()
        self.disconnect()

    def schedule_workers(self):
        """Schedule the workers and tasks. It is called after the connection
        is established."""
        self.tasks += [
            self.schedule(self.alisten()),
            self.schedule(self.arecv(self.reader)),
            self.schedule(self.asend(self.writer)),
        ]
        # self.send_init_packet()

    def cancel_workers(self):
        """Stop all the running workers."""
        for task in self.tasks:
            task.cancel()
        self.tasks.clear()

    # TODO; handle return on disconnect
    # returns b"" when connection is closed by server
    # TODO: fails when returns b"" causes the calle to raise error
    async def reader(self, n: int) -> bytes:
        """Reads n bytes from connection."""
        return await self.aread(n, self.loop)

    async def writer(self, d: bytes) -> None:
        """Writes data to connection."""
        return await self.awrite(d, self.loop)

    # def send_init_packet(self):
    #     """Send the init packet."""
    #     data = self.encode({
    #         "username": self.cfg("username"),
    #     })
    #     packet = PacketV1(
    #         type=PacketKind.INIT,
    #         data=data,
    #     )
    #     self.send_packet(packet)

    # def send_exit_packet(self):
    #     """Send the exit packet."""
    #     packet = PacketV1(
    #         type=PacketKind.EXIT,
    #         data=b"",
    #     )
    #     self.send_packet(packet)
