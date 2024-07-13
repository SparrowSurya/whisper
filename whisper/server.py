import asyncio
from typing import Dict, List

from .core import EventThread, StreamEncoder, StreamDecoder
from .core.server import BaseServer, ConnectionHandle, ServerConnection
from .core.logger import logger


# TODO - seperate thread to listen for keyboard interrupt when closing server.
class Server(EventThread, BaseServer):
    """Chat server backend.

    It manages the clients connected to the server and various kinds of
    requests coming from connections.
    """

    def __init__(self,
        host: str,
        port: int,
        encoding: str = "utf-8",
        chunk_size: int = 1024,
        connection: ServerConnection | None = None
    ):
        """
        Initialises the server settings.

        Arguments:
        * host - ip address of the server.
        * port - port address.
        * encoding - encoding used by the server.
        * chunk_size - amount of data to read from connection at a time.
        * connection - server connection manager object.
        """
        BaseServer.__init__(self, connection)
        EventThread.__init__(self)
        self.host = host
        self.port = port
        self.encoding = encoding
        self.chunk_size = chunk_size

        self.clients: List[ConnectionHandle] = []
        self.requests = {
            "hello": self.hello_request,
            "set-name": self.set_name_request,
            "exit": self.exit_request,
            "message": self.message_request,
        }

    async def listen(self):
        """
        Coroutine listening incoming requests. The connection is then
        passed to `handle` method which serves the connection.
        """
        logger.info("Listening for new connections ...")
        while True:
            try:
                conn = await self.accept()
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Exception while listening connections")
            else:
                self.schedule(self.handle(conn))
        logger.info("Stopped listening for new connections.")

    def register(self, conn: ConnectionHandle):
        """Register the connection."""
        self.clients.append(conn)

    def unregister(self, conn: ConnectionHandle):
        """Unregister the connection after closing it."""
        self.close(conn)
        self.clients.remove(conn)

    async def serve(self, conn: ConnectionHandle):
        """Coroutine listening the incoming data from connection and
        processing the request."""
        logger.info(f"Started serving: {conn.address}")
        decoder = StreamDecoder()
        try:
            while not conn.close:
                data = await self.read(conn, self.chunk_size)
                if data == b"":
                    logger.info(f"Received empty bytes from {conn.address}")
                    break
                if request := decoder.decode(data):
                    await self.recv(conn, **request)
        except asyncio.CancelledError:
            pass
        except Exception:
            logger.exception(f"Caught error while serving {conn.address}")
        finally:
            logger.info(f"Stopped serving {conn.address}")

    async def handle(self, conn: ConnectionHandle):
        """Handle newly connected connection."""
        self.register(conn)
        await self.serve(conn)
        self.unregister(conn)

    async def recv(self, conn: ConnectionHandle, **kwargs):
        """Process the request received from connection."""
        kind = kwargs.pop("kind")
        if func := self.requests.get(kind, None):
            if response := func(conn, **kwargs):
                logger.debug(f"Received '{kind}' request from {conn.address} kwargs: {kwargs}")
                await self.send(**response)
        else:
            logger.warning(f"Unknown 'kind': {kind}")

    async def send(self, **response):
        """Send the data to allowaed connections."""
        logger.debug(f"Sending: {response} to {[conn.name for conn in self.clients if conn.serve]}")
        encoder = StreamEncoder(**response)
        data = encoder.encode(self.encoding)
        for conn in self.clients:
            if conn.serve:
                await super().write(conn, data)

    def hello_request(self, conn: ConnectionHandle, **kwargs) -> Dict | None:
        """Response for `hello` request."""
        response = self.set_name_request(conn, **kwargs)
        conn.serve = True
        return response

    def set_name_request(self, conn: ConnectionHandle, name: str, **kwargs) -> Dict:
        """Response for 'set-name' request."""
        old_name = conn.username
        conn.data["username"] = name

        return {
            "kind": "message",
            "text": f"{old_name} renamed to {name}!" if old_name else f"{name} joined!",
            "user": None,
        }

    def exit_request(self, conn: ConnectionHandle, **kwargs) -> Dict | None:
        """Response for `exit` request."""
        conn.close = True
        if not conn.serve:
            return

        return {
            "kind": "message",
            "user": None,
            "text": f"{conn.username} exited!",
        }

    def message_request(self, conn: ConnectionHandle, text: str, **kwargs) -> Dict | None:
        """Response for `message` request."""
        if not conn.serve:
            return None

        return {
            "kind": "message",
            "user": conn.username,
            "text": text,
        }

    async def init_main(self):
        self.start_server(self.host, self.port)
        self.on_finish(self.connection.stop)
        await super().init_main()

    async def exit_main(self):
        self.stop_server()
        await super().exit_main()

    def init_coro(self):
        self.schedule(self.listen())
