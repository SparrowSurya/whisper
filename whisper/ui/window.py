import tkinter as tk

from .root import Root
from .theme import ThemeMixin
from .custom import CustomWindowMixin


class Window(CustomWindowMixin, tk.Tk, ThemeMixin):
    """Tkinter based GUI for the application."""

    DESTORY_EVENT = "<<Exit>>"

    __theme_attrs__ = {
        "background": "surfaceContainerLowest",
    }

    def __init__(self, title: str, *args, customize: bool = True, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        CustomWindowMixin.__init__(self, title, customize=customize)

        self.on_close(self.destroy)
        self.bind(self.DESTORY_EVENT, self.destroy)

        try:
            for widget in (
                self.n, self.s, self.e, self.w,
                self.ne, self.nw, self.se, self.sw,
            ):
                widget.__theme_attrs__ = self.titlebar.__theme_attrs__
        except AttributeError:
            pass

    def destroy(self, event=None):
        """Destroy the window."""
        super().destroy()

    def create_root(self, parent: tk.Misc) -> tk.Widget:
        return Root(parent)

    def set_title(self, title: str):
        """Sets title on the window."""
        self.wm_title(title)
