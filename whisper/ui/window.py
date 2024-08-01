import tkinter as tk

from .root import Root
from .theme import ThemeMixin
from .custom import CustomTkWindow


class Window(CustomTkWindow, ThemeMixin):
    """Tkinter based GUI for the application."""

    DESTORY_EVENT = "<<Exit>>"

    __theme_attrs__ = {
        "background": "surfaceContainerLowest",
    }

    def __init__(self, title: str, *args, **kwargs):
        CustomTkWindow.__init__(self)

        self.title(title)
        self.bind(self.DESTORY_EVENT, self.destroy)

        if self.is_customized:
            self.on_close(self.destroy)
            for widget in (
                self.grip_n, self.grip_s, self.grip_e, self.grip_w,
                self.grip_ne, self.grip_nw, self.grip_se, self.grip_sw,
            ):
                widget.__theme_attrs__ = self.titlebar.__theme_attrs__
        else:
            self.wm_protocol("WM_DELETE_WINDOW", self.destroy)

    def destroy(self, event=None):
        """Destroy the window."""
        super().destroy()

    def mainloop(self):
        """Window mainloop."""
        super().mainloop()

    def get_root(self, parent: tk.Misc | None = None) -> tk.Widget:
        return Root(self)
