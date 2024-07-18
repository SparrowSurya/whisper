import tkinter as tk

from whisper.ui.widgets import Frame, Text, Button
from whisper.ui.utils import dynamic_text_height


class InputPanel(Frame):
    """
    Chat input panel for input from user.

    User inputs:
    * textinput - contains text message.
    * sendbtn - sends the message.
    """

    __theme_attrs__ = {
        "background": "surfaceContainer",
    }

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.textinput = Text(
            self,
            highlightthickness=1,
            insertwidth=2,
            insertborderwidth=0,
            wrap="word",
            height=1,
            font=("Roboto", 16, "normal"),
        )

        self.blank_img = tk.PhotoImage()
        self.sendbtn = Button(
            self,
            image=self.blank_img,
            compound="center",
            relief="flat",
            text="",
            border=0,
            borderwidth=0,
            highlightthickness=0,
            font=("Roboto", 32, "bold"),
            height=26,
            width=26,
        )

        self.textinput.grid(row=0, column=0, sticky="nsew")
        self.sendbtn.grid(row=0, column=1, sticky="new")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=self.sendbtn.winfo_width() + 40)

        self.textinput.bind(
            "<KeyRelease>",
            lambda _: dynamic_text_height(self.textinput, 5),
            "+",
        )
        self.sendbtn.bind("<FocusIn>", lambda _:self.textinput.focus_set(), "+")

        self.textinput.__theme_attrs__ = {
            "background": "surfaceContainerLow",
            "foreground": "onSecondaryContainer",
            "insertbackground": "onSecondaryContainer",
            "selectbackground": "onSecondaryContainer",
            "selectforeground": "surfaceContainerLow",
            "highlightbackground": "primaryContainer",
            "highlightcolor": "primaryContainer",
        }

        self.sendbtn.__theme_attrs__ = {
            "activebackground": "surfaceContainer",
            "activeforeground": "primary",
            "background": "surfaceContainer",
            "foreground": "primaryContainer",
            "highlightcolor": "surfaceContainer",
            "highlightbackground": "surfaceContainer",
        }

    def get_text(self) -> str:
        """Text entered."""
        return self.textinput.get("1.0", "end-1c")

    def clear(self):
        """Cleans the text content."""
        self.textinput.delete("1.0", "end")
        self.textinput.configure(height=1)
