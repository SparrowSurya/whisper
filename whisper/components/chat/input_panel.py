from tkinter import PhotoImage

from ui.widgets import Frame, Button
from whisper.components.textinput import MultilineTextInput


class InputPanel(Frame):
    """
    Chat input panel for input from user.

    User inputs:
    * textinput - contains text message.
    * sendbtn - sends the message.
    """

    __theme_attrs__ = {
        "background": "surfaceContainerLow",
    }

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.textinput = MultilineTextInput(
            self,
            highlightthickness=0,
            insertwidth=1,
            insertborderwidth=0,
            wrap="word",
            height=1,
            font=("Roboto", 16, "normal"),
            padx=4,
            pady=4,
        )

        self.blank_img = PhotoImage()
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

        self.sendbtn.bind("<FocusIn>", lambda _: self.textinput.focus_set(), "+")

        self.textinput.__theme_attrs__ = {
            "background": "surface",
            "foreground": "onSurface",
            "selectbackground": "onSurface",
            "selectforeground": "surface",
            "insertbackground": "onSurfaceVariant",
        }

        self.sendbtn.__theme_attrs__ = {
            "activebackground": "surfaceContainerLow",
            "activeforeground": "primary",
            "background": "surfaceContainerLow",
            "foreground": "primaryContainer",
            "highlightcolor": "surfaceContainerLow",
            "highlightbackground": "surfaceContainerLow",
        }

    def get_text(self) -> str:
        """Text entered."""
        return self.textinput.get("1.0", "end-1c")

    def clear(self):
        """Cleans the text content."""
        self.textinput.delete("1.0", "end")
        self.textinput.configure(height=1)
