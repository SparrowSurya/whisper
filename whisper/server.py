import asyncio
import threading
from typing import List, Tuple

from .core import EventThread, StreamEncoder, StreamDecoder
from .core.server import BaseServer, ConnectionHandle, ServerConnection, Response
from .core.logger import logger
from .settings import CHUNK_SIZE, ENCODING, TIMEOUT


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

        self.exit_reason = None
        self.clients: List[ConnectionHandle] = []
        self.requests = {
            "hello": self.hello_request,
            "set-name": self.set_username_request,
            "exit": self.exit_request,
            "message": self.message_request,
        }

    def valid_username(self, username: str) -> bool:
        """Validates given username."""
        # limitied character set
        for ch in username:
            if not (ch.isalnum() or ch in "-_."):
                return False

        # name should not be taken by other client
        name = username.lower()
        for client in self.clients:
            if client.serve and client.username.lower() == name:
                return False
        return True

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
        """Unregister the connection and close it."""
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

    def hello_request(self,
        conn: ConnectionHandle,
        **kwargs,
    ) -> Tuple[Response] | None:
        """Response for `hello` request.

        Client must provide a valid username to be served.

        Valid `hello` Request:
        >>> {
        >>>     "kind": "hello",
        >>>     "name": "<name>",
        >>> }

        Responses:
        * set-name & chat-info: to sender
        * user-join: to other
        """
        responses = self.set_username_request(conn, **kwargs)
        if not responses:
            return None

        users = tuple(
            client.username for client in self.clients
            if client.serve and not client.close
        )

        response3 = Response(
            content={
                "kind": "chat-info",
                "users": users,
            },
            receivers=(conn,),
        )

        self.remove_timeout(conn)
        conn.serve = True
        return *responses, response3

    def set_username_request(self,
        conn: ConnectionHandle, name: str,
        **kwargs,
    ) -> Tuple[Response] | None:
        """Response for 'set-username' request.

        This can be used to set new or rename exisitng username. The
        given username is verified for validity.

        Valid `set-username` request:
        >>> {
        >>>     "kind": "set-username",
        >>>     "username": "<username>",
        >>> }

        Responses:
        * set-username; to sender
        * user-rename: to other
        """
        old = conn.username
        new = name.strip()
        if not self.valid_username(new):
            return None # TODO - provide error response

        conn.username = new
        response1 = Response(
            content={
                "kind": "set-username",
                "name": new,
            },
            receivers=(conn,),
        )

        # user is joined or renamed
        if old is None:
            response2 = Response(
                content={
                    "kind": "user-join",
                    "user": new,
                },
                receivers=tuple(self.clients),
            )
        else:
            response2 = Response(
                content={
                    "kind": "user-rename",
                    "old": old,
                    "new": new,
                },
                receivers=tuple(client for client in self.clients if client != conn),
            )

        return response1, response2

    def exit_request(self,
        conn: ConnectionHandle,
        reason: str = "",
        **kwargs,
    ) -> Tuple[Response] | Response | None:
        """Response for `exit` request.

        This removes the user from chat and closes connection. Client is
        responsible for managing the updation of users in chat.

        Valid `exit` request:
        >>> {
        >>>     "kind": "exit",
        >>>     "reason": "[reason]",
        >>> }

        Response:
        * user-exit - to others
        """
        conn.close = True
        if not conn.serve:
            return None

        conn.serve = False
        response = Response(
            content = {
                "kind": "user-exit",
                "user": conn.username,
            },
            receivers = tuple(client for client in self.clients if client != conn),
        )
        return response

    def message_request(self,
        conn: ConnectionHandle,
        text: str,
        **kwargs,
    ) -> Response | None:
        """Response for `message` request.

        Valid `message` request:
        >>> {
        >>>     "kind": "message",
        >>>     "text": "<text message>",
        >>> }

        Response:
        * message - to all
        """
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

    def remove_timeout(self, conn: ConnectionHandle):
        """Removes timeout on user."""
        conn.data.pop("timeout").cancel()
        logger.debug(f"Timeout removed for {conn.address}")

    async def timeout_handler(self, conn: ConnectionHandle):
        """Coroutine that manages timeout on a connection."""
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
            self.exit_reason = "force shutdown"
        except Exception as error:
            logger.exception(f"Server crash due to {type(error).__name__}")
            self.exit_reason = "server crash"
        finally:
            self.stop()
            thread.join()
            logger.info(f"{thread.name} joined!")

    async def inform_exit(self):
        """Informs the connections about the server exit."""
        await self.send(
            Response(
                content={
                    "kind": "exit",
                    "reason": self.exit_reason,
                },
                receivers=self.clients,
            )
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
