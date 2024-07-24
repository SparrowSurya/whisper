import threading
from typing import Self

from .client import Client
from .ui.window import Window
from .core.logger import logger
from .settings import DEFAULT_THEME


class ClientApp(Client, Window):
    """Client side tkinter based GUI.

    The app contains refrence to itself `app` and should be passed to
    components down the root component.
    """
    def __init__(self, title: str, host: str, port: int, username: str, customize: bool = True):
        """
        Arguments:
        * title - title on the window.
        * host - server hostname.
        * port - server port address.
        * username - client username.
        * customize - use custom window.
        """
        Client.__init__(self, host, port, username)
        Window.__init__(self, title, customize=customize)
        self.theme = DEFAULT_THEME
        self.__exiting = False
        self.setup()

    @property
    def app(self) -> Self:
        """A refrence to itself."""
        return self

    def run(self):
        """Run the client application.."""
        thread = threading.Thread(target=self.start, name="Asyncio-Thread")
        try:
            thread.start()
            logger.info(f"Started {thread.name}")
            self.mainloop()
        except BaseException:
            logger.exception("Caught error while running")
            self.prepare_exit()
            self.mainloop()
        finally:
            thread.join()
            logger.info(f"{thread.name} joined!")

    def setup(self):
        """Initiate all setup and configurations."""
        self.apply_config()
        self.on_close(self.prepare_exit)
        self.on_finish(lambda _: self.event_generate(self.DESTORY_EVENT))

    def prepare_exit(self):
        """Close application gracefully."""
        if not self.__exiting:
            logger.info("preparing for exit")
            self.send("exit", on_done=lambda _: self.stop())
            self.__exiting = True

    def apply_config(self):
        """Apply the configured settings application."""
        self.geometry(400, 500, 30, 30, center=True)
        self.root.chat.topbar.set_username(self.username)
        self.apply_theme(self.theme)

        # to remove focus on username when somewhere else is clicked
        self.bind_all("<Button-1>", lambda event: event.widget.focus_set(), "+")

        # remove focus from custom titlebar buttons if exists
        try:
            self.titlebar.minimize.bind("<FocusIn>", lambda _:self.focus_set(), "+")
            self.titlebar.maximize.bind("<FocusIn>", lambda _:self.focus_set(), "+")
            self.titlebar.close.bind("<FocusIn>", lambda _:self.focus_set(), "+")
        except AttributeError:
            pass

    def show_message(self, **kwargs):
        """Shows the message in chat.

        Arguments:
        * kwargs - related information.
        """
        self.root.chat.show_message(**kwargs)

    def update_username(self, name: str, **kwargs):
        """Update the username."""
        Client.update_username(self, name, **kwargs)
        self.root.chat.update_username(name)

    def server_exit(self, **kwargs):
        """Server is closing."""
        logger.info("Server is closing")
        self.prepare_exit()

    async def init_main(self):
        await super().init_main()

        # show the server address on topbar
        ip, port = self.servername()
        self.root.chat.topbar.set_servername(f"{ip}:{port}")