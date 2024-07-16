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

    def __init__(self, host: str, port: int, username: str, **kwargs):
        """
        Arguments:
        * host - server hostname.
        * port - server port address.
        * username - client username.
        """
        Client.__init__(self, host, port, username, **kwargs)
        Window.__init__(self)
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
        self.setup_root()
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
        self.set_title("Whisper")
        self.set_geometry(400, 500, 30, 30)
        self.root.chat.topbar.set_title(self.username)
        self.apply_theme(self.theme)

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
