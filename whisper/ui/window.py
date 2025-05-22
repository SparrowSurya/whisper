"""
This module provide custom tkinter window and toplevel window.
"""

import logging
import tkinter as tk
import tkinter.font as tkfont
from typing import Callable, Unpack, Mapping

from .custom import CustomWidget
from .event_bind import EventBinding
from whisper.typing import (
    TkPalette as _TkPalette,
    Font as _Font,
    PaletteOpts as _PaletteOpts,
    WindowColorAttr as _ColorAttr,
    Misc as _Misc,
)


logger = logging.getLogger(__name__)


class CustomWindow(CustomWidget):
    """A mixin class for tkinter window."""

    WINDOW_EXIT_EVENT = "<<Exit-Window>>"
    """Custom window exit event."""

    TclError = tk.TclError
    """Exception base class raised by GUI"""

    def __init__(self):
        CustomWidget.__init__(self)
        self.exit_event = EventBinding(self, self.WINDOW_EXIT_EVENT, self.destroy)
        self.on_window_exit(self.destroy)

    def __init_subclass__(cls):
        if not issubclass(cls, (tk.Tk, tk.Toplevel)):
            logger.warning(f"{cls} is not subclass of `tkinter.Tk` or `tkinter.Toplevel`")

    def hide_window(self):
        """Hide the window."""
        self.wm_withdraw()

    def show_window(self):
        """Show the window."""
        self.wm_deiconify()

    def show_titlebar(self):
        """Shows the titlebar on the window."""
        self.wm_overrideredirect(False)

    def hide_titlebar(self):
        """Hides titlebar on the window."""
        self.wm_overrideredirect(True)

    def on_window_exit(self, callback: Callable[[], None]):
        """
        Register a callback function, invoked when window is closed via close button.
        Callback is not invoked when `destory` or `quit` methods are used.
        """
        self.wm_protocol("WM_DELETE_WINDOW", callback)

    def set_palette(self, *args, **kwargs: Unpack[_TkPalette]):
        """Sets tkinter palette options.."""
        self.tk_setPalette(self, *args, **kwargs)

    @classmethod
    def default_colorscheme(cls) -> Mapping[_ColorAttr, _PaletteOpts]:
        return {
            "background": "base",
            "highlightbackground": "base",
            "highlightcolor": "base",
        }


class MainWindow(tk.Tk, CustomWindow):
    """Main tkinter window which supports custom themes."""

    def __init__(self):
        tk.Tk.__init__(self)
        CustomWindow.__init__(self)

    def mainloop(self, n: int = 0):
        """Start mainloop of the tkinter window."""
        tk.Tk.mainloop(self, n)

    def set_font(self, font_name: str = "*", **options: Unpack[_Font]):
        """Set font options. Make sure that font_name should be valid tkinter font name"""
        if font_name == "*":
            for name in tkfont.names(self):
                font = tkfont.nametofont(name, self)
                font.configure(**options)
        else:
            font = tkfont.nametofont(font_name, self)
            font.configure(**options)


class Window(tk.Toplevel, CustomWindow):
    """Toplevel tkinter window which supports custom theme."""

    def __init__(self, master: _Misc):
        tk.Toplevel.__init__(self, master)
        CustomWindow.__init__(self)
