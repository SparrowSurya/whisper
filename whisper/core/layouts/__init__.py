import tkinter as tk

from whisper.core.components.base.container import Container
from whisper.core.components.chat import ChatBox


class Root(Container):
    """Root widget of the application."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.chatbox = ChatBox(self)
        self.chatbox.pack(fill=tk.BOTH, expand=tk.TRUE)
