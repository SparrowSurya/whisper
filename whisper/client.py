import asyncio
import threading
from typing import Self

from .core.client_connection import ClientConnection
from .core.streamcodec import StreamEncoder, StreamDecoder, Message
from .core.event_thread import EventThread
from .ui.window import Window


class ClientApp(EventThread, Window):
    """Client side tkinter based GUI.

    The app contains refrence to itself `app` and should be passed to
    components down the root component.
    """

    def __init__(self, host: str, port: int, username: str):
        """
        Arguments:
        * host - server hostname.
        * port - server port address.
        * username - client username.
        """
        EventThread.__init__(self)
        Window.__init__(self)

        self.host = host
        self.port = port
        self.username = username
        self.encoding = "utf-8"
        self.__exiting = False
        self.conn = ClientConnection()

        self.setup()

    @property
    def app(self) -> Self:
        """A refrence to itself."""
        return self

    def run(self):
        """Run the client application.."""
        thread = threading.Thread(target=self.start, name="Event-Thread")
        try:
            thread.start()
            self.mainloop()
        except BaseException:
            self.prepare_exit()
            self.mainloop()
        finally:
            thread.join()

    async def send(
        self,
        kind: str,
        encoding: str = "utf-8",
        **kwargs,
    ):
        """
        Send message to the server.

        Arguments:
        * kind - message or some action.
        * kwargs - related info.
        """
        obj = Message.create(kind, **kwargs)
        encoder = StreamEncoder(obj)
        data = encoder.encode(encoding)
        await self.conn.write(data)

    async def listen(self):
        """
        Listens incoming data from server.
        Content is passed to the `recv` method.
        """
        decoder = StreamDecoder()
        try:
            while self.conn.is_connected:
                if (data := await self.conn.read(4096)) == b"":
                    break
                obj = decoder.decode(data)
                if obj is not None:
                    self.recv(**obj._asdict()) # type: ignore
        except asyncio.CancelledError:
            pass
        except Exception as err:
            pass

    def recv(self, **kwargs: object):
        """
        Reads the message and performs the functionality.

        Arguments:
        * kwargs - content received from server.
        """
        kind = kwargs.pop("kind", None)

        if kind == "message":
            self.show_message(**kwargs)
        elif kind == "set-name":
            self.update_username(**kwargs)

    def setup(self):
        """Initiate all setup and configurations."""
        self.setup_root()
        self.apply_config()
        self.on_close(self.prepare_exit)
        self.on_finish(lambda _: self.event_generate(self.DESTORY_EVENT))

    async def init_main(self):
        """See `EventThread.init_main`."""
        await self.conn.connect(
            host=self.host,
            port=self.port,
            loop=self.loop,
        )

    def init_coro(self):
        """See `EventThread.init_coro`."""
        self.schedule(self.send("set-name", name=self.username))
        self.schedule(self.listen())

    async def exit_main(self):
        """See `EventThread.exit_main`."""
        await self.conn.disconnect()

    def prepare_exit(self):
        """Close application gracefully."""
        if not self.__exiting:
            self.schedule(
                self.send("exit", self.encoding),
                on_done=lambda _: self.stop(),
            )
            self.__exiting = True

    def apply_config(self):
        """Apply the configured settings application."""
        self.set_title("Whisper")
        self.set_geometry(400, 500, 30, 30)
        self.root.chat.topbar.set_title(self.username)

    def show_message(self, **kwargs):
        """
        Shows the message in chat.

        Arguments:
        * kwargs - related information.
        """
        self.root.chat.show_message(**kwargs)

    def update_username(self, name: str, **kwargs):
        """Update the username."""
        self.username = name
        self.root.chat.update_username(name)
