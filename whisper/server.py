import asyncio
import threading
from typing import List, Iterable

from .core import EventThread, StreamEncoder, StreamDecoder
from .core.server import BaseServer, ConnectionHandle, ServerConnection, Response
from .core.logger import logger
from .settings import CHUNK_SIZE, ENCODING, TIMEOUT


# TODO - seperate thread to listen for keyboard interrupt when closing server.
class Server(EventThread, BaseServer):
    """Chat server backend.

    It manages the clients connected to the server and various kinds of
    requests coming from connections.
    """

    def __init__(
        self,
        host: str,
        port: int,
        encoding: str = ENCODING,
        chunk_size: int = CHUNK_SIZE,
        timeout: int = TIMEOUT,
        connection: ServerConnection | None = None,
    ):
        """
        Initialises the server settings.

        Arguments:
        * host - ip address of the server.
        * port - port address.
        * encoding - encoding used by the server.
        * chunk_size - amount of data to read from connection at a time.
        * timeout - time period to send valid hello request.
        * connection - server connection manager object.
        """
        BaseServer.__init__(self, connection)
        EventThread.__init__(self)
        self.host = host
        self.port = port
        self.encoding = encoding
        self.chunk_size = chunk_size
        self.timeout = timeout

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
                conn.data["future"] = self.schedule(self.handle(conn))
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
        self.set_timeout(conn)
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
            logger.debug(
                f"Received '{kind}' request from {conn.address} kwargs: {kwargs}"
            )
            if responses := func(conn, **kwargs):
                if isinstance(responses, Response):
                    await self.send(responses)
                else:
                    await self.send(*responses)
        else:
            logger.warning(f"Unknown 'kind': {kind}")

    async def send(self, *responses: Response):
        """Send the response to target connections."""
        for response in responses:
            logger.debug(f"Sending: {response}")
            encoder = StreamEncoder(**response.content)
            data = encoder.encode(self.encoding)
            for conn in response.receivers:
                if conn.serve:
                    await super().write(conn, data)

    def hello_request(self, conn: ConnectionHandle, **kwargs) -> Iterable[Response] | Response | None:
        """Response for `hello` request."""
        response = self.set_name_request(conn, **kwargs)
        if response:
            conn.data.pop("timeout").cancel()
            logger.debug(f"Timeout removed for {conn.address}")
            conn.serve = True
            return response
        return None

    def set_name_request(self, conn: ConnectionHandle, name: str, **kwargs) -> Iterable[Response]:
        """Response for 'set-name' request."""
        old_name = conn.username
        conn.data["username"] = name

        content1 = {
            "kind": "message",
            "text": f"{old_name} renamed to {name}!" if old_name else f"{name} joined!",
            "user": None,
        }
        receivers1 = tuple(client for client in self.clients)

        content2 = {
            "kind": "set-name",
            "name": conn.data["username"],
        }
        receivers2 = (conn,)

        return (
            Response(content2, receivers2),
            Response(content1, receivers1),
        )

    def exit_request(self, conn: ConnectionHandle, **kwargs) -> Iterable[Response] | Response | None:
        """Response for `exit` request."""
        conn.close = True
        if not conn.serve:
            return None

        conn.serve = False
        content = {
            "kind": "message",
            "user": None,
            "text": f"{conn.username} exited!",
        }
        receivers = tuple(client for client in self.clients if client != conn)
        return Response(content, receivers)

    def message_request(
        self, conn: ConnectionHandle, text: str, **kwargs
    ) -> Response | None:
        """Response for `message` request."""
        if not conn.serve:
            return

        content = {
            "kind": "message",
            "user": conn.username,
            "text": text,
        }
        receivers = tuple(client for client in self.clients)
        return Response(content, receivers)

    def set_timeout(self, conn: ConnectionHandle):
        """Set timeout on user withhin the period it must send valid hello request."""
        coro = self.timeout_handler(conn)
        fut = self.schedule(coro)
        conn.data["timeout"] = fut
        logger.debug(f"Timeout {self.timeout}s set on {conn.address}")

    async def timeout_handler(self, conn: ConnectionHandle):
        """COroutine that manages timeout on a connection."""
        await asyncio.sleep(self.timeout)
        if conn.data.get("timeout", None):
            conn.close = True
            conn.serve = False
            logger.debug(f"Timeout expired for {conn.address}")
            conn.data.pop("future").cancel()

    def run(self):
        """Run the server."""
        thread = threading.Thread(target=self.start, name="Async-Thread")
        try:
            thread.start()
            logger.info(f"Started {thread.name}")

            # TODO - use signals
            # example - https://github.com/dask/distributed/blob/main/distributed/_signals.py
            while thread.is_alive():
                thread.join(timeout=1)

        except KeyboardInterrupt:
            logger.info("Caught Keyboard Interrupt - closing the server")
            self.stop()
        finally:
            thread.join()
            logger.info(f"{thread.name} joined!")

    async def inform_exit(self):
        """Informs the connections about the shutdown."""
        await self.send(
            Response({"kind": "exit"}, self.clients)
        )

    async def init_main(self):
        self.start_server(self.host, self.port)
        await super().init_main()

    def init_coro(self):
        self.schedule(self.listen())

    async def exit_main(self):
        await self.inform_exit()
        for conn in self.clients:
            conn.data["future"].cancel()
        self.stop_server()
        await super().exit_main()
