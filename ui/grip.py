import tkinter as tk
from typing import Callable

from .widgets import Frame


class Grip(Frame):
    """A grip widget for resizing the window."""

    __theme_attrs__ = {
        "background": "surfaceContainerLowest",
    }

    cursors = {
        "n": "top_side",
        "s": "bottom_side",
        "e": "right_side",
        "w": "left_side",
        "ne": "top_right_corner",
        "nw": "top_left_corner",
        "se": "bottom_right_corner",
        "sw": "bottom_left_corner",
    }

    def __init__(self, master: tk.Misc, *args, anchor: str, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.anchor = anchor
        self._bind_id = None

    def enable(self, callback: Callable[[str, tk.Event], None]):
        """Enable the grip resizing."""
        self._bind_id = self.bind("<Button-1>", lambda e: callback(self.anchor, e))
        self.config(cursor=self.cursors[self.anchor])

    def disable(self):
        """Disable grip resizing."""
        self.unbind("<Button-1>", self._bind_id)
        self.config(cursor="")
        self._bind_id = None
