import asyncio
import concurrent.futures
from typing import Callable

from .core.client import BaseClient
from .core.streamcodec import StreamEncoder, StreamDecoder
from .core.event_thread import EventThread
from .core.logger import logger


class Client(EventThread, BaseClient):
    """The class provides the client backend functions."""

    def __init__(self, host: str, port: int, username: str, **kwargs):
        """
        Arguments:
        * host - server host address.
        * port - server port address.
        * username - client username.
        """
        BaseClient.__init__(self, None)
        EventThread.__init__(self)
        self.host = host
        self.port = port
        self.username = username
        self.encoding = "utf-8"
        self.chunk_size = 1024
        self.response = {
            "message": self.show_message,
            "set-name": self.update_username,
        }

    def send(self,
        kind: str,
        on_done: Callable[[concurrent.futures.Future[None]], None] | None = None,
        **kwargs,
    ):
        """Send serialised message to the server."""
        kwargs["kind"] = kind
        logger.debug(f"Sending {kwargs}")
        encoder = StreamEncoder(**kwargs)
        data = encoder.encode(self.encoding)
        self.schedule(self.write(data), on_done)

    async def listen(self):
        """Listen incoming data from server."""
        logger.info("Started listening data")
        decoder = StreamDecoder()
        try:
            while self.is_connected:
                # TODO - ConnectionAbortedError when client disconnects
                data = await self.read(self.chunk_size)
                if data == b"":
                    logger.info("Received b''")
                    break
                if response := decoder.decode(data):
                    self.recv(**response)
        except asyncio.CancelledError:
            pass
        except Exception:
            logger.exception("Caught error while listening data")
        finally:
            logger.info("Stopped listening data")

    def recv(self, **kwargs: object):
        """Reads message and performs action/updation."""
        logger.debug(f"Received {kwargs}")
        kind = kwargs.pop("kind", None)
        if func := self.response.get(kind, None):
            func(**kwargs)
        else:
            logger.warning(f"Unknows `{kind}` response from server, kwargs: {kwargs}")

    async def init_main(self):
        self.connect(
            host=self.host,
            port=self.port,
            loop=self.loop,
        )
        await EventThread.init_main(self)

    def init_coro(self):
        EventThread.init_coro(self)
        self.schedule(self.listen())
        self.send("hello", name=self.username)

    async def exit_main(self):
        self.disconnect()
        await EventThread.exit_main(self)

    def update_username(self, name: str, **kwargs):
        """Updates username."""
        self.username = name

    def show_message(self, user: str | None, text: str):
        """Show the message on chat."""
