import tkinter as tk
from typing import Any, Self

from ui.window import TkWindow
from ui.messagebox import ShowInfo, ShowWarning, ShowError

from whisper.settings import TITLEBAR_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from whisper.utils.binding import Binding
from whisper.components.titlebar import Titlebar
from whisper.components.root import Root


class MainApplication(TkWindow):
    """
    Main application.
    """

    DESTROY_EVENT = "<<MainWindowDestroy>>"

    def __init__(self, title: str):
        super().__init__(title=title)
        self.destroy_bind = Binding(self, self.DESTROY_EVENT, self.destroy, bind=True)

        if self.is_modified:
            self.titlebar.config_theme()
            self.set_minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

    @property
    def app(self) -> Self:
        return self

    def destroy(self, event: Any = None):
        """Destroy the window."""
        super().destroy()

    def mainloop(self):
        """TKinter mainloop."""
        super().mainloop()

    def create_root(self, parent: tk.Misc | None = None) -> Root:
        """Root widget of the application."""
        if hasattr(self, "root"):
            return self.root
        return Root(parent or self)

    def create_titlebar(self, parent: tk.Misc | None = None) -> Titlebar:
        """Titlebar of the application (only for modified window)."""
        if hasattr(self, "titlebar"):
            return self.titlebar
        return Titlebar(parent or self, height=TITLEBAR_HEIGHT)

    def info_dialog(self, title: str, msg: str) -> ShowInfo:
        """Display information dialog."""
        return ShowInfo(self, title, msg)

    def warning_dialog(self, title: str, msg: str) -> ShowWarning:
        """Display warning dialog."""
        return ShowWarning(self, title, msg)

    def error_dialog(self, title: str, msg: str) -> ShowError:
        """Display error dialog."""
        return ShowError(self, title, msg)
