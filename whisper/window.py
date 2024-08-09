import tkinter as tk

from ui.window import TkWindow
from .components.root import Root
from .components.titlebar import Titlebar
from whisper.settings import TITLEBAR_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT


class Window(TkWindow):
    """Tkinter based GUI for the application."""

    DESTORY_EVENT = "<<Exit>>"

    __theme_attrs__ = {
        "background": "surfaceContainerLowest",
    }

    def __init__(self, title: str, *args, **kwargs):
        TkWindow.__init__(self, title, *args, **kwargs)

        self.bind(self.DESTORY_EVENT, self.destroy)

        if self.is_modified:
            self.titlebar.config_theme()
            self.set_minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

    def destroy(self, event=None):
        """Destroy the window."""
        super().destroy()

    def mainloop(self):
        """Window mainloop."""
        super().mainloop()

    def create_root(self, parent: tk.Misc | None = None) -> Root:
        if hasattr(self, "root"):
            return self.root
        return Root(parent or self)

    def create_titlebar(self, parent: tk.Misc | None = None) -> Titlebar:
        if hasattr(self, "titlebar"):
            return self.titlebar
        return Titlebar(parent or self, height=TITLEBAR_HEIGHT)
