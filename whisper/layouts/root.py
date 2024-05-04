import tkinter as tk

from whisper.components.base import Container
from whisper.components.chat import Chat


class Root(Container):
    """Root widget of the application."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = self.master.app  # type: ignore

        self.chat = Chat(self)
        self.chat.pack(fill=tk.BOTH, expand=tk.TRUE)
