from whisper.core.chat import BaseChat
from ui.widgets import Frame
from .topbar import TopBar
from .view import View
from .input_panel import InputPanel


class Chat(Frame, BaseChat):
    """Chat ui component.

    Children:
    * topbar - header for the chat.
    * view - shows the chat messages.
    * input - for user input.
    """

    __theme_attrs__ = {
        "background": "surfaceContainerLowest",
    }

    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        BaseChat.__init__(self, self.master.app)

        self.topbar = TopBar(self, pady=4, padx=4)
        self.view = View(self)
        self.input = InputPanel(self, padx=4, pady=4)

        self.topbar.grid(row=0, column=0, sticky="nsew")
        self.view.grid(row=1, column=0, sticky="nsew")
        self.input.grid(row=2, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, minsize=self.input.winfo_height())
        self.grid_columnconfigure(0, weight=1)

        self.input.sendbtn.config(command=self.send_message)

    def send_message(self, event=None):
        """Event listener to send message."""
        if text := self.input.get_text().strip():
            super().send_message(text=text)
            self.input.clear()

    def show_message(self, user: str | None, text: str, **kwargs):
        """Shows the message on the chat."""
        self.view.show_message(user, text)

    def show_info(self, message: str):
        """Shows the information on chat."""
        self.view.show_info(message)

    def update_username(self, name: str, **kwargs):
        """Change the displayed username."""
        self.topbar.set_username(name)
