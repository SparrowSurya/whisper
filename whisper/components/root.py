import tkinter as tk

from ui.widgets import Frame
from .chat import Chat


class Root(Frame):
    """Root widget of the application."""

    __theme_attrs__ = {
        "background": "surfaceContainerLowest",
    }

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = self.master.app

        self.chat = Chat(self)
        self.chat.pack(fill=tk.BOTH, expand=tk.TRUE)
