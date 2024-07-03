from typing import Dict, Any

from whisper.core.chat import BaseChat
from whisper.ui.widgets import Frame
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

    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        BaseChat.__init__(self, self.master.app)

        self.topbar = TopBar(self)
        self.view = View(self)
        self.input = InputPanel(self)

        self.topbar.grid(row=0, column=0, sticky="nsew")
        self.view.grid(row=1, column=0, sticky="nsew")
        self.input.grid(row=2, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, minsize=self.input.winfo_height())
        self.grid_columnconfigure(0, weight=1)

        self.input.sendbtn.config(command=self.send_message)
        self.input.textinput.focus()

    def send_message(self, event=None):
        """Event listener to send message."""
        if text := self.input.get_text().strip():
            super().send_message(text=text)
            self.input.clear()

    def show_message(self, user: str | None, text: str, **kwargs):
        """Shows the message on the chat."""
        if user is None:
            self.view.show_info(text)
        else:
            self.view.show_message(user, text)

    def update_username(self, name: str, **kwargs):
        """Change the displayed username."""
        self.topbar.set_title(name)

    @property
    def _cnf(self) -> Dict[str, Any]:
        return {
            "bg": "#343145",
        }