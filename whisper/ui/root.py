import tkinter as tk

from .widgets.frame import Frame
from .chat import Chat


class Root(Frame):
    """Root widget of the application."""

    __theme_attrs__ = {
        "background": "surfaceContainerLowest",
    }

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = self.master.app  # type: ignore

        self.chat = Chat(self)
        self.chat.pack(fill=tk.BOTH, expand=tk.TRUE)
