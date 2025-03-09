"""
This module contains the customised version of tkinter windows.
"""

import logging
import tkinter as tk
from typing import Callable

from whisper.utils.binding import Binding


logger = logging.getLogger(__name__)


class MainWindow(tk.Tk):
    """Main tkinter window object (inherits `tkinter.Tk`)."""

    WINDOW_EXIT = "<<Exit>>"
    """Custom window exit event."""

    def __init__(self):
        super().__init__()
        self.exit_binding = Binding(self, self.WINDOW_EXIT, self.exit_window)
        self.on_window_exit(self.quit)

    def on_window_exit(self, callback: Callable[[], None]):
        """
        Registers a callback function to be invoked when window is
        closed using close button. Uses `tkinter.Tk.wm_protocol`.
        """
        self.wm_protocol("WM_DELETE_WINDOW", callback)

    def exit_window(self):
        """Destroy the window."""
        super().destroy()
        logger.debug("Window Destroy")

    def mainloop(self, n: int = 0):
        """Start mainloop of the tkinter window."""
        logger.debug("Mainloop Begin")
        super().mainloop(n)
        logger.debug("Mainloop Finish")

    def quit(self):
        """
        Exit the window wihtout invoking the `on_window_exit` callback.
        """
        super().quit()
        logger.debug("Window Quit")

    def setup_root(self):
        """Setups the root widget of the window and its children."""


class Window(tk.Toplevel):
    """Toplevel tkinter window object (inherits `tk.Toplevel`)."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = master.app
