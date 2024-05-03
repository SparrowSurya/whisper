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
        self.view = View(self, state="disabled")
        self.input = InputPanel(self)

        self.topbar.pack(fill="x", expand=0)
        self.view.pack(fill="both", expand=1)
        self.input.pack(fill="x", expand=0)

        self.input.sendbtn.config(command=self.on_send)
        self.input.textinput.bind("<Return>", self.on_send)
        self.input.textinput.focus()

    def on_send(self, event=None):
        """Event listener to send message."""
        text = self.input.textinput.get().strip()
        if text:
            content = self.create_content(text=text)
            BaseChat.send(self, content)
            self.input.clear()

    def recv(self, content: Dict[str, Any]):
        """Shows the message on the chat."""
        user, msg = content["user"], content["text"]
        if user is None:
            self.view.show_info(msg)
        else:
            self.view.show_message(user, msg)
