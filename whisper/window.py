import tkinter as tk

from .ui.root import Root
from .ui.window import TkWindow


class Window(TkWindow):
    """Tkinter based GUI for the application."""

    DESTORY_EVENT = "<<Exit>>"

    __theme_attrs__ = {
        "background": "surfaceContainerLowest",
    }

    def __init__(self, title: str, *args, **kwargs):
        TkWindow.__init__(self, title, *args, **kwargs)

        self.bind(self.DESTORY_EVENT, self.destroy)
        self.on_close(self.destroy)

        if self.is_custom_window:
            self.titlebar.config_theme()

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
