from ui.widgets import Frame, Label


class Info(Frame):
    """Display the information in chat."""

    __theme_attrs__ = {
        "background": "surfaceContainerHigh"
    }

    def __init__(self, master, *args, info: str, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.body = Label(
            self,
            text=info,
            justify="center",
            anchor="center",
            font=("Roboto", 14, "normal"),
        )
        self.body.pack(fill="x", anchor="center")
        self.body.bind(
            "<Configure>",
            lambda e: self.body.configure(wraplength=self.body.master.winfo_width()),
            "+",
        )

        self.body.__theme_attrs__ = {
            "background": "surfaceContainerHigh",
            "foreground": "onSurfaceVariant",
        }