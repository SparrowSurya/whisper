import asyncio


class Stream:
    """
    This provides an asynchronous interface to read and write to
    asyncio streams.
    """

    __slots__ = ("__connected", "reader", "writer", "proto", "transport")

    def __init__(self):
        self.__connected = False

    @property
    def is_open(self) -> bool:
        """If stream objects are initialised."""
        return self.__connected

    async def open(
        self, host: str, port: int, loop: asyncio.AbstractEventLoop, **kwargs
    ):
        """
        Open connection and initialize the stream objects.

        Arguments:
        * host - host address.
        * port - port number.
        * kwargs - see `asyncio.loop.create_connection()`.
        """
        if self.is_open:
            raise RuntimeError("Already an established connection.")

        reader = asyncio.StreamReader(limit=2**16, loop=loop)
        proto = asyncio.StreamReaderProtocol(reader, loop=loop)
        transport, _ = await loop.create_connection(
            lambda: proto, host, port, **kwargs
        )
        writer = asyncio.StreamWriter(
            transport, proto, reader, loop
        )
        self._create(reader=reader, writer=writer, proto=proto, transport=transport)

    async def close(self):
        """Close connection and stream objects."""
        if not self.is_open:
            raise RuntimeError("No established connection")

        self.__connected = False
        self.writer.close()
        await self.writer.wait_closed()
        self._destroy()

    async def read(self, size: int) -> bytes:
        """Read the data received from server."""
        return await self.reader.read(size)

    async def write(self, data: bytes):
        """Sends the data to server."""
        self.writer.write(data)
        await self.writer.drain()

    def _create(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        proto: asyncio.StreamReaderProtocol,
        transport: asyncio.Transport,
    ):
        self.writer = writer
        self.reader = reader
        self.proto = proto
        self.transport = transport
        self.__connected = True

    def _destroy(self):
        self.__connected = False
        del self.writer, self.reader, self.proto, self.transport
