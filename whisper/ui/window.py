import tkinter as tk
from typing import Callable

from .root import Root
from .theme import ThemeMixin


class Window(tk.Tk, ThemeMixin):
    """Tkinter based GUI for the application."""

    DESTORY_EVENT = "<<Exit>>"

    __theme_attrs__ = {
        "background": "surfaceContainerLowest",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_close(self.destroy)
        self.bind(self.DESTORY_EVENT, self.destroy)

    def on_close(self, callback: Callable[[], None]):
        """Callback when user clicks the close button.
        Callback must destroy the window manually."""
        self.wm_protocol("WM_DELETE_WINDOW", callback)

    def destroy(self, event=None):
        """Destroy the window."""
        super().destroy()

    def setup_root(self):
        """Setups the root and children widgets."""
        self.root = Root(self)
        self.root.pack(fill=tk.BOTH, expand=tk.TRUE)

    def set_title(self, title: str):
        """Sets title on the window."""
        self.wm_title(title)

    def set_geometry(self, width: int, height: int, x: int, y: int):
        """Sets the dimensions and position of the window.

        Arguments:
        * width - width of the window.
        * height - height of the window.
        * x - top left corner of the window.
        * y - bottom-right corener of the window.
        """
        self.wm_geometry(f"{width}x{height}+{x}+{y}")
