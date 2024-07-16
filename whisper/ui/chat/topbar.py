from whisper.ui.widgets import Frame, Label


class TopBar(Frame):
    """
    Chat topbar which contains some userful things.

    Useful things:
    * title - display the title on chat.
    """

    __theme_attrs__ = {
        "background": "primaryContainer",
    }

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.title = Label(
            self,
            text="",
            justify="left",
            anchor="w",
            font=("Roboto", 14, "bold"),
        )
        self.title.pack(side="left", fill="x")
        self.title.__theme_attrs__ = {
            "background": "primaryContainer",
            "foreground": "primary",
        }

    def set_title(self, title: str):
        """Sets the title on header."""
        self.title.config(text=title.capitalize())