import tkinter.font as tkfont
from typing import Dict, Any

from whisper.core.chat import BaseChat
from whisper.components.base import Container
from .topbar import TopBar
from .view import View
from .input_panel import InputPanel


class Chat(Container, BaseChat):
    """Manages the chat and actions.

    Widgets
    -------
    * topbar - cotnains the brief info about chat.
    * view - shows the messages in the chat.
    * input - for user input and actions.
    """

    def __init__(self, master, *args, **kwargs):
        Container.__init__(self, master, *args, **kwargs)
        BaseChat.__init__(self, self.master.app)  # type: ignore

        self.topbar = TopBar(self)
        self.view = View(self)
        self.input = InputPanel(self)

        self.topbar.grid(row=0, column=0, sticky="nsew")
        self.view.grid(row=1, column=0, sticky="nsew")
        self.input.grid(row=2, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, minsize=self.input.winfo_height())
        self.grid_columnconfigure(0, weight=1)

        self.input.sendbtn.config(command=self.on_send)
        self.input.textinput.focus()

    def on_send(self, event=None):
        """Event listener to send message."""
        text = self.input.get_text().strip()
        if text:
            content = self.create_content(text=text)
            BaseChat.send(self, content)
            self.input.clear()
            self.input.textinput.configure_height(5)

    def recv(self, content: Dict[str, Any]):
        """Shows the message on the chat."""
        user, msg = content["user"], content["text"]
        if user is None:
            self.view.show_info(msg)
        else:
            self.view.show_message(user, msg)

    @property
    def _cnf(self) -> Dict[str, Any]:
        return {
            "bg": "#343145",
        }
