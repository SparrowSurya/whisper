import tkinter as tk
from typing import Any, Dict

from whisper.components.base import ScrollableContainer
from .message import Message
from .info import Info


class View(ScrollableContainer):
    """Chat view. Contains chat messages."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, cnf=self._cnf, **kwargs)
        self.frame.config(cnf=self._cnf)
        self._canvas.config(bg=self.frame.cget("bg"))
        self._listen_scroll(self.frame)

    def show_message(self, user: str, message: str):
        """Message sent by user."""
        self._pack(Message(self.frame, username=user, message=message))

    def show_info(self, info: str):
        """Message to inform everyone."""
        self._pack(Info(self.frame, info=info))

    def _pack(self, widget: tk.Widget):
        """Pack a widget inside."""
        widget.pack(fill="x", expand=1, pady=2)
        self._listen_scroll(widget)
        self.scroll_to_bottom()

    def _listen_scroll(self, widget: tk.Widget):
        """Listens scroll on widget and its children (recursive)."""
        childs = [widget]
        while len(childs) > 0:
            w = childs.pop(0)
            w.bindtags(("scroll",) + w.bindtags())
            childs.extend(w.winfo_children())

    @property
    def _cnf(self) -> Dict[str, Any]:
        return {
            "bg": "#252331",
            "padx": 2,
            "pady": 2,
        }
