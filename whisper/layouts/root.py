import tkinter as tk
from typing import Any, Dict

from whisper.components.base import Container
from whisper.components.chat import Chat


class Root(Container):
    """Root widget of the application."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, cnf=self._cnf, **kwargs)
        self.app = self.master.app  # type: ignore

        self.chat = Chat(self)
        self.chat.pack(fill=tk.BOTH, expand=tk.TRUE)

    @property
    def _cnf(self) -> Dict[str, Any]:
        return {
            "bg": "#252331",
            "padx": 2,
            "pady": 2,
        }
