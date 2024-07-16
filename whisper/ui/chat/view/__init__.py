import tkinter as tk

from whisper.ui.widgets import ScrollableFrame
from .message import Message
from .info import Info


class View(ScrollableFrame):
    """It displays various kinds of messages in chat."""

    __theme_attrs__ = {
        "background": "surfaceContainerLowest"
    }

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = self.master.app
        self._frame.config(bg=self._frame.cget("bg"))
        self._canvas.config(bg=self._frame.cget("bg"))
        self._listen_scroll(self._frame)

    def show_message(self, user: str, message: str):
        """Message sent by user."""
        self._pack(Message(self._frame, username=user, message=message))

    def show_info(self, info: str):
        """Message to inform everyone."""
        self._pack(Info(self._frame, info=info))

    def _pack(self, widget: tk.Widget):
        """Pack a widget inside."""
        widget.apply_theme(self.app.theme)
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
