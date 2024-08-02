import asyncio
import concurrent.futures
from typing import Callable, List

from .core.client import BaseClient
from .core.streamcodec import StreamEncoder, StreamDecoder
from .core.event_thread import EventThread
from .core.logger import logger
from .settings import CHUNK_SIZE, ENCODING


class Client(EventThread, BaseClient):
    """The class provides the client backend functions."""

    def __init__(self,
        host: str,
        port: int,
        username: str,
        chunk_size: str = CHUNK_SIZE,
        encoding: str = ENCODING,
        **kwargs,
    ):
        """
        Arguments:
        * host - server host address.
        * port - server port address.
        * username - client username.
        * chunk_size - amount to data read at once,
        * encoding - encoding for object serialization.
        """
        BaseClient.__init__(self, None)
        EventThread.__init__(self)
        self.host = host
        self.port = port
        self.username = username
        self.encoding =encoding
        self.chunk_size = chunk_size

        self.response = {
            "message": self.show_message,
            "set-username": self.update_username,
            "exit": self.server_exit,
            "chat-info": self.update_chat_info,
            "user-rename": self.user_renamed,
            "user-join": self.user_joined,
            "user-exit": self.user_exited,
        }
        self.others = []

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
                data = await self.read(self.chunk_size)
                if data == b"":
                    logger.info("Received b''")
                    break
                if response := decoder.decode(data):
                    self.recv(**response)
        except asyncio.CancelledError:
            pass
        except ConnectionAbortedError:
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
        """Response for `set-username`. Updates username."""
        self.username = name

    def show_message(self, user: str | None, text: str):
        """Response for `message`. Does nothing!"""

    def server_exit(self, reason: str = "", **kwargs):
        """Response `exit` from server. Server is closing due to some reason."""
        if reason:
            logger.info(f"Server closing due to {reason}")
        self.stop()

    def update_chat_info(self, users: List[str], **kwargs):
        """Response `chat-info` from server. Information about the chat."""
        self.others = users

    def user_joined(self, user: str, **kwargs):
        """Response `user-join` from server. Updates the users list."""
        self.others.append(user)

    def user_exited(self, user: str, reason: str = "", **kwargs):
        """Response `user-exit` from server. Updates users list."""
        self.others.remove(user)

    def user_renamed(self, old: str, new: str, **kwargs):
        """Response `user-rename` from server. Updates user in users list."""
        self.others.remove(old)
        self.others.append(new)