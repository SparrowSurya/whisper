import tkinter as tk
from typing import Any, Dict

from whisper.ui.widgets import Frame, Text, Button
from whisper.ui.utils import dynamic_text_height


class InputPanel(Frame):
    """
    Chat input panel for input from user.

    User inputs:
    * textinput - contains text message.
    * sendbtn - sends the message.
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, cnf=self._cnf, **kwargs)

        self.textinput = Text(
            self,
            fg="#b8b8b8",
            bg="#252331",
            selectforeground="#252331",
            selectbackground="#b8b8b8",
            highlightbackground="#b8b8b8",
            highlightcolor="#184ef6",
            highlightthickness=1,
            insertbackground="#b8b8b8",
            insertwidth=2,
            insertborderwidth=0,
            wrap="word",
            height=1,
            font=("Roboto", 16, "normal"),
        )
        self.send_icon = tk.PhotoImage(file="./whisper/assets/send.png")
        self.sendbtn = Button(
            self,
            image=self.send_icon,
            compound="center",
            relief="flat",
            bg="#252331",
            activebackground="#252331",
            bd=0,
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

    def get_text(self) -> str:
        """Text entered."""
        return self.textinput.get("1.0", "end-1c")

    def clear(self):
        """Cleans the text content."""
        self.textinput.delete("1.0", "end")
        self.textinput.configure(height=1)

    @property
    def _cnf(self) -> Dict[str, Any]:
        return {
            "bg": "#252331",
        }
