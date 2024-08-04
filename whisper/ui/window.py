import tkinter as tk

from .custom import TitlebarMixin


class TkWindow(TitlebarMixin, tk.Tk):
    """Custom tkinter window with custom titlebar."""

    def __init__(self, title: str, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        TitlebarMixin.__init__(self)
        self.title(title)
        self.on_close(self.destroy)


class ToplevelWindow(TitlebarMixin, tk.Toplevel):
    """Custom tkinter toplevel window with custom titlebar."""

    def __init__(self, title: str, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        TitlebarMixin.__init__(self)
        self.title(title)
