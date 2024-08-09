import threading
from typing import Self

from .client import Client
from .window import Window
from .core.logger import logger
from .settings import DEFAULT_THEME, DEFAULT_ICON_PATH


class ClientApp(Client, Window):
    """Client side tkinter based GUI.

    The app contains refrence to itself `app` and should be passed to
    components down the root component.
    """
    def __init__(self, title: str, host: str, port: int, username: str):
        """
        Arguments:
        * title - title on the window.
        * host - server hostname.
        * port - server port address.
        * username - client username.
        * customize - use custom window.
        """
        Client.__init__(self, host, port, username)
        Window.__init__(self, title)
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
        except BaseException as error:
            if not isinstance(error, KeyboardInterrupt):
                logger.exception("Caught error while running")
            else:
                logger.info("Caught KeyboardInterrput")
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
        self.root.chat.input.textinput.focus_force()

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

        if self.is_modified:
            # removes focus from custom titlebar buttons if exists
            self.titlebar.set_icon(DEFAULT_ICON_PATH)
            self.titlebar.minimize.bind("<FocusIn>", lambda _:self.focus_set(), "+")
            self.titlebar.maximize.bind("<FocusIn>", lambda _:self.focus_set(), "+")
            self.titlebar.close.bind("<FocusIn>", lambda _:self.focus_set(), "+")

    def show_message(self, **kwargs):
        """Shows the message in chat.

        Arguments:
        * kwargs - related information.
        """
        self.root.chat.show_message(**kwargs)

    def update_username(self, name: str, **kwargs):
        """Update the username."""
        changed = name != self.username
        Client.update_username(self, name, **kwargs)
        if changed:
            self.root.chat.update_username(name)
            self.root.chat.show_info(f"you renamed to {name}")

    def server_exit(self, reason: str = "", **kwargs):
        """Server is closing."""
        if reason:
            logger.info(f"Server closing due to {reason}")
        self.prepare_exit()

    async def init_main(self):
        await super().init_main()

        # show the server address on topbar
        ip, port = self.servername()
        self.root.chat.topbar.set_servername(f"{ip}:{port}")

    def user_joined(self, user: str, **kwargs):
        if user == self.username:
            self.root.chat.show_info("You joined!")
        else:
            super().user_joined(user, **kwargs)
            self.root.chat.show_info(f"{user} joined!")

    def user_exited(self, user: str, reason: str = "", **kwargs):
        super().user_exited(user, reason, **kwargs)
        self.root.chat.show_info(f"{user} left!")

    def user_renamed(self, old: str, new: str, **kwargs):
        super().user_renamed(old, new, **kwargs)
        self.root.chat.show_info(f"{old} renamed to {new}!")