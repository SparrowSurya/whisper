import tkinter.font as tkfont

from whisper.components.base import Container, Label


class TopBar(Container):
    """Top bar for the chat.
    Contains the essentials items on the top of chat.

    Child
    -----
    * title - title for the chat.

    Methods
    -------
    * set_title - sets the title of the chat.
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.title = Label(
            self,
            text="",
            justify="left",
            anchor="w",
            bg="#343145",
            fg="#ffffff",
            font=tkfont.Font(family="Roboto", size=12, weight="bold"),
        )
        self.title.pack(side="left", fill="x")

    def set_title(self, title: str):
        """Sets the title on header."""
        self.title.config(text=title)
