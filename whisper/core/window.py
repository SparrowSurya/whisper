import tkinter as tk

from whisper.core.layouts import Root


class Window(tk.Tk):
    """Tkinter user interface for the application."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_title(self, title: str):
        """Sets title on the window."""
        self.wm_title(title)

    def set_geometry(self, width: int, height: int, x: int, y: int):
        """Sets the geometry of the window.

        Arguments:
        * width: width of the window.
        * height: height of the window.
        * x: top left corner of the window.
        * y: bottom-right corener of the window.
        """
        self.wm_geometry(f"{width}x{height}+{x}+{y}")

    def setup_root(self):
        """Setups the root element of the window."""
        self.root = Root(self)
        self.root.pack(fill=tk.BOTH, expand=tk.TRUE)

    def late_setup(self):
        """Setup before running event loop of the window."""
        pass
