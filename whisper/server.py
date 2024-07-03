import asyncio
from typing import Tuple, List

from .core.client_handler import ConnHandle
from .core.streamcodec import StreamEncoder, StreamDecoder, Message


class Server:
    """Asynchronous Chat Server."""

    def __init__(self, host: str, port: int):
        """
        Arguments:
        * host - server's ip address
        * port - port number
        """
        self.host = host
        self.port = port
        self.server: asyncio.Server | None = None
        self.encoding = "utf-8"
        self.conns: List[ConnHandle] = []
        self.chunk_size = 1024

    @property
    def is_serving(self) -> bool:
        """Is server running."""
        if self.server is None:
            return False
        return self.server.is_serving()

    @property
    def address(self) -> Tuple[str, int]:
        """Address of the server."""
        if self.server is None:
            raise RuntimeError("Server is not running.")
        return self.server.sockets[0].getsockname()

    def register(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> ConnHandle:
        """Register the connection and provides a Handler to it."""
        conn = ConnHandle(reader=reader, writer=writer)
        self.conns.append(conn)
        return conn

    async def unregister(self, conn: ConnHandle):
        """Unregister the connection handler."""
        conn.writer.close()
        await conn.writer.wait_closed()
        self.conns.remove(conn)

    async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle newly connected client."""
        conn = self.register(reader=reader, writer=writer)
        decoder = StreamDecoder()

        try:
            while conn.run:
                if (data := await conn.read(self.chunk_size)) == b"":
                    break
                if (obj := decoder.decode(data)) is not None:
                    await self.process(obj, conn)
        except asyncio.CancelledError:
            pass
        except Exception as error:
            pass
        finally:
            conn.writer.close()
            await conn.writer.wait_closed()
            self.conns.remove(conn)

    async def broadcast(self, data: bytes):
        """Send the data to each connection."""
        for conn in self.conns:
            await conn.write(data)

    async def process(self, obj: object, conn: ConnHandle):
        """This processes the incoming request from connection."""
        kwargs = obj._asdict()  # type: ignore
        kind = kwargs.pop("kind")

        if kind == "set-name":
            await self.process_name(conn, kwargs["name"])
        elif kind == "exit":
            await self.process_exit(conn)
        elif kind == "message":
            await self.process_message(conn, kwargs["text"])

    async def process_name(self, conn: ConnHandle, new_name: str) -> object:
        """Responds the request to change name."""
        old_name = conn.username
        conn.insert("username", new_name)

        if old_name is not None:
            text = f"{old_name} changed to {new_name}!"
        else:
            text = f"{new_name} joined!"

        response = Message.message(
            text=text,
            user=None,
        )
        encoder = StreamEncoder(response)
        await self.broadcast(encoder.encode(self.encoding))

    async def process_exit(self, conn: ConnHandle) -> object | None:
        """Responds the request to exit."""
        conn.run = False
        if conn.username is None:
            return

        text = f"{conn.username} exited"
        response = Message.message(
            user=None,
            text=text,
        )
        encoder = StreamEncoder(response)
        await self.broadcast(encoder.encode(self.encoding))

    async def process_message(self, conn: ConnHandle, text: str) -> object | None:
        """Responds the request to send message."""
        name = conn.username
        if name is None:
            return

        response = Message.message(
            user=conn.username,
            text=text,
        )
        encoder = StreamEncoder(response)
        await self.broadcast(encoder.encode(self.encoding))

    async def run(self):
        """Run chat server."""
        self.server = await asyncio.start_server(self.handle, self.host, self.port)
        async with self.server:
            await self.server.serve_forever()
        self.server = None
