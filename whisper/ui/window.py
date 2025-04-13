"""
This module provide custom tkinter window and toplevel window.
"""

import tkinter as tk
from typing import Callable

from whisper.ui.typing import TkPaletteOpts
from .custom import CustomWidget
from .utils import Binding


class MainWindow(tk.Tk, CustomWidget):
    """Main tkinter window which supports custom themes."""

    WINDOW_EXIT_EVENT = "<<Exit-MainWindow>>"
    """Custom window exit event."""

    def __init__(self):
        tk.Tk.__init__(self)
        CustomWidget.__init__(self)
        self.exit_event = Binding(self, self.WINDOW_EXIT_EVENT, self.quit)
        self.on_window_exit(self.quit)

    def on_window_exit(self, callback: Callable[[], None]):
        """Registers a callback function to be invoked when window is closed using
        close button. Uses `tkinter.Tk.wm_protocol`."""
        self.wm_protocol("WM_DELETE_WINDOW", callback)

    def mainloop(self, n: int = 0):
        """Start mainloop of the tkinter window."""
        tk.Tk.mainloop(self, n)

    def quit(self):
        """Exit the window wihtout invoking the `on_window_exit` callback."""
        tk.Tk.destroy(self)

    def set_palette(self, **options: TkPaletteOpts):
        """Sets tkinter palette options. Do not provide empty values."""
        tk.Tk.tk_setPalette(self, **options)



class Window(tk.Toplevel, CustomWidget):
    """Toplevel tkinter window which supports custom theme."""

    WINDOW_EXIT_EVENT = "<<Exit-Window>>"
    """Custom window exit event."""

    def __init__(self, master: tk.Misc):
        tk.Toplevel.__init__(self, master)
        CustomWidget.__init__(self)
        self.exit_event = Binding(self, self.WINDOW_EXIT_EVENT, self.quit)
        self.on_window_exit(self.quit)

    def on_window_exit(self, callback: Callable[[], None]):
        """Registers a callback function to be invoked when window is closed using
        close button. Uses `tkinter.Tk.wm_protocol`."""
        self.wm_protocol("WM_DELETE_WINDOW", callback)

    def quit(self):
        """Exit the window wihtout invoking the `on_window_exit` callback."""
        tk.Toplevel.destroy()

    def set_palette(self, **options: TkPaletteOpts):
        """Sets tkinter palette options. Do not provide empty values."""
        tk.Toplevel.tk_setPalette(self, **options)
