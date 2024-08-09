from ui.widgets import Frame, Label


class Message(Frame):
    """Text message from a user in chat."""

    __theme_attrs__ = {
        "background": "surfaceContainerHigh"
    }

    def __init__(self, master, *args, username: str, message: str, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.head = Label(
            self,
            text=username,
            height=1,
            justify="left",
            anchor="nw",
            font=("Roboto", 14, "bold", "underline"),
        )
        self.body = Label(
            self,
            text=message,
            justify="left",
            anchor="nw",
            font=("Roboto", 14, "normal"),
        )

        self.head.pack(fill="x", anchor="nw")
        self.body.pack(fill="x", anchor="sw")

        self.body.bind(
            "<Configure>",
            lambda e: self.body.config(wraplength=self.body.master.winfo_width()),
            "+",
        )

        self.head.__theme_attrs__ = {
            "background": "surfaceContainerHigh",
            "foreground": "primary",
        }

        self.body.__theme_attrs__ = {
            "background": "surfaceContainerHigh",
            "foreground": "onSurface",
        }