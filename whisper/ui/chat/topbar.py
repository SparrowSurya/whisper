from whisper.ui.widgets import Frame, Entry, Label


class TopBar(Frame):
    """
    Chat topbar contaning info about chat.
    """

    __theme_attrs__ = {
        "background": "surfaceContainerLow",
    }

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = self.master.app

        self.username = Entry(
            self,
            justify="left",
            font=("Roboto", 14, "bold"),
            state="disabled",
            relief="flat",
            insertwidth=1,
            insertborderwidth=0,
        )
        self.servername = Label(
            self,
            justify="left",
            font=("Roboto", 14, "normal"),
        )

        self.username.pack(side="left", fill="x")
        self.servername.pack(side="right")

        self.username.__theme_attrs__ = {
            "disabledbackground": "surfaceContainer",
            "disabledforeground": "onSurface",
            "background": "surfaceContainer",
            "foreground": "onSurface",
            "insertbackground": "onSurfaceVariant",
        }
        self.servername.__theme_attrs__ = {
            "background": "surfaceContainer",
            "foreground": "onSurface",
        }

        self.username.bind("<Double-Button-1>", self.enable_edit_username)
        self.username.bind("<FocusOut>", self.disable_edit_username)
        self.username.bind("<Escape>", self.disable_edit_username)
        self.username.bind("<Return>", self.change_username)

    def set_servername(self, name: str):
        """Sets the username."""
        self.servername.config(text=name)

    def set_username(self, name: str):
        """Sets the username."""
        self.username.config(state="normal")
        self.username.delete(0, "end")
        self.username.insert(0, name)
        self.username.config(state="disabled")

    def enable_edit_username(self, event=None):
        self.username.config(state="normal")

    def disable_edit_username(self, event=None):
        self.username.delete(0, "end")
        self.username.insert(0, self.app.username)
        self.username.config(state="disabled")

    def change_username(self, event=None):
        name = self.username.get().strip()
        if name and name != self.app.username:
            self.app.send("set-name", name=name)
        self.disable_edit_username()
