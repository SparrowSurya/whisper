import tkinter as tk

from .window import ToplevelWindow
from .widgets import Label, Button, Frame
from whisper.settings import DEFAULT_ICON_PATH


class DialogBox(ToplevelWindow):
    """Base dialog box for popups.

    This class is a mix of `ToplevelWindow` and `ThemeMixin`.
    It supports the customised and uncustomised window.
    """

    def __init__(self, master: tk.Misc, title: str):
        """
        Master should be the custom window.

        Additionaly, hides the minimize and maximize buttons if
        possible.
        """
        super().__init__(title)
        self.master = master
        if self.is_custom_window:
            self.theme = self.master.theme
            self.titlebar.config_theme()
            self.titlebar.set_icon(DEFAULT_ICON_PATH)
            self.titlebar.hide_minimize()
            self.titlebar.hide_maximize()
            self.disable_resize()
        self.geometry(300, 200, center=True)
        self.grab_set()


class MessageBox(DialogBox):
    """Displays message with an icon."""

    def __init__(self,
        master: tk.Misc,
        title: str,
        message: str = "",
        glyph_icon: str = "",
    ):
        super().__init__(master, title)
        self.glyph_icon = glyph_icon
        self.text_msg = message
        self.configure_widgets()
        if hasattr(self.master, "theme"):
            self.apply_theme(self.master.theme)

    def setup_widgets(self):
        """Setups the widgets."""
        super().setup_widgets()
        self.setup_local_widgets()

    def setup_local_widgets(self):
        """Creates the message widgets."""
        self.box1 = Frame(self.root, padx=5, pady=5)
        self.box2 = Frame(self.root, padx=16, pady=8)

        self.icon = Label(self.box1, font=("Roboto", 64, "bold"))
        self.message = Label(self.box1, font=("Roboto", 12, "normal"), wraplength=360, justify="left")
        self.submit = Button(self.box2, font=("Roboto", 12, "normal"), padx=24, borderwidth=0)

        self.box1.pack(fill="both", expand=1)
        self.box2.pack(fill="x", expand=1)

        self.icon.grid(row=0, column=0, sticky="nse", padx=10)
        self.message.grid(row=0, column=1, sticky="nsw", padx=10)
        self.submit.pack(side="right")

        self.box1.grid_columnconfigure(0, weight=2)
        self.box1.grid_columnconfigure(1, weight=8)

    def configure_widgets(self):
        """Confiugre the widgets."""
        self.icon.config(text=self.glyph_icon)
        self.message.config(text=self.text_msg)
        self.submit.config(text="Ok", command=self.destroy)

        self.root.__theme_attrs__ = {
            "background": "surface",
        }

        self.box1.__theme_attrs__ = {
            "background": "surface",
        }
        self.box2.__theme_attrs__ = {
            "background": "surfaceContainer",
        }

        self.icon.__theme_attrs__ = {
            "background": "surface",
        }
        self.message.__theme_attrs__ = {
            "background": "surface",
            "foreground": "onSurface",
        }
        self.submit.__theme_attrs__ = {
            "background": "surfaceContainerHighest",
            "foreground": "onSurface",
        }

    def destroy(self) -> None:
        self.grab_release()
        self.master.focus_force()
        super().destroy()


GLYPH_ICON_INFO = ""
GLYPH_ICON_WARNING = ""
GLYPH_ICON_ERROR = ""
GLYPH_ICON_QUESTION = ""


class ShowInfo(MessageBox):
    """Shows the information dialog."""

    def __init__(self, master: tk.Misc, title: str, message: str = ""):
        super().__init__(master, title, message, GLYPH_ICON_INFO)

    def configure_widgets(self):
        super().configure_widgets()
        self.icon.config(fg="#3e72ff")


class ShowWarning(MessageBox):
    """Shows the warning dialog."""

    def __init__(self, master: tk.Misc, title: str, message: str = ""):
        super().__init__(master, title, message, GLYPH_ICON_WARNING)

    def configure_widgets(self):
        super().configure_widgets()
        self.icon.config(fg="#ffbc00")


class ShowError(MessageBox):
    """Shows the error dialog."""

    def __init__(self, master: tk.Misc, title: str, message: str = ""):
        super().__init__(master, title, message, GLYPH_ICON_ERROR)

    def configure_widgets(self):
        super().configure_widgets()
        self.icon.config(fg="#ff0f0f")
