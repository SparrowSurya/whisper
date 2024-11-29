import asyncio
import logging
from typing import Awaitable, Callable, Tuple

from whisper.core.packet import Packet
from whisper.utils.decorators import aworker
from .connection import ClientConn


logger = logging.getLogger(__name__)


class BaseClient:
    """
    Base Client class capable of connecting and communicating to server.
    """

    def __init__(self, tcp_conn: ClientConn | None = None):
        """Initialises the tcp connection.

        Argument:
        * tcp_conn - client tcp connection.
        """
        self.connection = tcp_conn or ClientConn()
        self.sendq: asyncio.Queue[Packet] = asyncio.Queue()
        self.recvq: asyncio.Queue[Packet] = asyncio.Queue()

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self.connection.is_connected

    def server_address(self) -> Tuple[str, int]:
        """Provides the server address."""
        return self.connection.sock.getpeername()

    def connect(self, host: str, port: int):
        """Connect to the server.

        Arguments:
        * host - server ip address.
        * port - server port address.

        Raises:
        * RuntimeError - if client is already connected.
        * ConnectionRefusedError - if unable to connect.
        """
        logger.debug(f"Client connecting to {(host, port)}")
        self.connection.connect(host, port)
        logger.debug(f"Client connected to {(host, port)}")

    def disconnect(self):
        """Close the connection.

        Raises:
        * RuntimeError - client is not connected.
        """
        self.connection.disconnect()
        logger.info("Client connection closed")

    @aworker("PacketReader", logger=logger)
    async def arecv(self, reader: Callable[[int], Awaitable[bytes]]):
        """Coroutine reading incoming packets from the server."""
        while True:
            packet = await Packet.from_stream(reader)
            await self.recvq.put(packet)
            logger.debug(f"Received: {packet!r}")

    @aworker("PacketWriter", logger=logger)
    async def asend(self, writer: Callable[[bytes], Awaitable[None]]):
        """Coroutine writing packets to the server."""
        while True:
            packet = await self.sendq.get()
            data = packet.to_stream()
            await writer(data)
            logger.debug(f"Sent: {packet!r}")

    async def aread(self,
        n: int,
        loop: asyncio.AbstractEventLoop,
    ) -> bytes:
        """Read n bytes from the server."""
        return await self.connection.read(n, loop)

    async def awrite(self, data: bytes, loop: asyncio.AbstractEventLoop):
        """Write data to the server."""
        return await self.connection.write(data, loop)
