import asyncio


# TODO
# * what happens if connection cannot be established
# * what if read or write fails (eg - reading b"" from server)
class ClientConnection:
    """It provides asynchronous interface for client connection.

    Methods:
    * connect - connect to server.
    * disconnect - disconnect from server.
    * write - send raw bytes to server.
    * read - receive raw bytes from server.
    * is_connected - check if connection has been established.
    """

    __slots__ = ("__connected", "__reader", "__writer", "__protocol", "__transport")

    def __init__(self):
        self.__connected = False

    @property
    def is_connected(self) -> bool:
        """
        Check if connection is established or initialized.

        NOTE - This does not means that data can be sent out
        to server sucessfully.
        """
        return self.__connected

    async def connect(
        self, host: str, port: int, loop: asyncio.AbstractEventLoop, **kwargs
    ):
        """
        Establish connection with server.

        Arguments:
        * host - server hostname.
        * port - server port address.
        * kwargs - see `asyncio.loop.create_connection()`.

        Raises:
        * RuntimeError - if connection already established.
        """
        if self.is_connected:
            raise RuntimeError("Already an established connection.")

        reader = asyncio.StreamReader(limit=2**16, loop=loop)
        protocol = asyncio.StreamReaderProtocol(reader, loop=loop)
        transport, _ = await loop.create_connection(
            lambda: protocol, host, port, **kwargs
        )
        writer = asyncio.StreamWriter(transport, protocol, reader, loop)
        self._create(
            reader=reader, writer=writer, protocol=protocol, transport=transport
        )

    async def disconnect(self):
        """Close connection.

        Raises:
        * RuntimeError - if connection is not established.
        """
        if not self.is_connected:
            raise RuntimeError("No established connection")

        self.__connected = False
        self.__writer.close()
        await self.__writer.wait_closed()
        self._destroy()

    async def read(self, n: int) -> bytes:
        """Read `n` bytes of data received from server."""
        return await self.__reader.read(n)

    async def write(self, data: bytes):
        """Sends the data to server."""
        self.__writer.write(data)
        await self.__writer.drain()

    def _create(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        protocol: asyncio.StreamReaderProtocol,
        transport: asyncio.Transport,
    ):
        self.__writer = writer
        self.__reader = reader
        self.__protocol = protocol
        self.__transport = transport
        self.__connected = True

    def _destroy(self):
        self.__connected = False
        del self.__writer, self.__reader, self.__protocol, self.__transport
