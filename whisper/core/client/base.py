import asyncio

from .connection import ClientConnection
from ..logger import logger


class BaseClient:
    """
    The class provides the basic functionality for client. Its purpose
    is to server minimum essential functions.
    """

    def __init__(self, connection: ClientConnection | None = None):
        """Initialises the connection object.

        Argument:
        * connection - object to manage the client connection.
        """
        self.connection = connection or ClientConnection()
        self._loop = None

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Running asyncio event loop. If is not set then the loop is
        set ro running event loop,

        Raises:
        * RuntimeError - if not event loop was found.
        """
        if self._loop is None:
            self.loop = asyncio.get_running_loop()
        return self._loop

    @loop.setter
    def loop(self, loop: asyncio.AbstractEventLoop):
        """Set asyncio event loop."""
        self._loop = loop


    @property
    def is_connected(self) -> bool:
        """Check is client is connected."""
        return self.connection.is_connected

    def connect(self,
        host: str,
        port: int,
        loop:
        asyncio.AbstractEventLoop | None = None,
    ):
        """Connect to the server.

        Arguments:
        * host - server ip address.
        * port - server port address.
        * loop - running asyncio event loop.

        Raises:
        * RuntimeError - if client is already connected.
        * ConnectionRefusedError - if unable to connect.
        """
        self._loop = loop
        self.connection.connect(host, port)
        logger.info(f"Client connected to {(host, port)}")

    def disconnect(self):
        """Close the connection.

        Raises:
        * RuntimeError - client is not connected.
        """
        self.connection.disconnect()
        logger.info("Client connection closed")

    async def read(self, n: int):
        """Read n bytes from the server."""
        return await self.connection.read(n, self.loop)

    async def write(self, data: bytes):
        """Write data to the server."""
        return await self.connection.write(data, self.loop)
