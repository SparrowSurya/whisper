import tkinter as tk
from typing import Callable

from whisper.layouts import Root


class Window(tk.Tk):
    """Tkinter based graphical user interface ofor the application."""

    DESTORY_EVENT = "<<Exit>>"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_close(self.destroy)
        self.bind(self.DESTORY_EVENT, self.destroy)

    def on_close(self, callback: Callable[[], None]):
        """When user clicks the close button. Callback must destroy the window manually."""
        self.wm_protocol("WM_DELETE_WINDOW", callback)

    def destroy(self, event=None):
        """Destroy the window."""
        super().destroy()

    def setup_root(self):
        """Setups the root element of the window."""
        self.root = Root(self, bg="#252331", padx=2, pady=2)
        self.root.pack(fill=tk.BOTH, expand=tk.TRUE)

    def set_title(self, title: str):
        """Sets title on the window."""
        self.wm_title(title)

    def set_geometry(self, width: int, height: int, x: int, y: int):
        """Sets the geometry of the window.

        Arguments:
        * width - width of the window.
        * height - height of the window.
        * x - top left corner of the window.
        * y - bottom-right corener of the window.
        """
        self.wm_geometry(f"{width}x{height}+{x}+{y}")
