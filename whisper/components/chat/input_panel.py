import tkinter.font as tkfont

from whisper.components.base import Container, TextInput, Button


class InputPanel(Container):
    """Contains the various of input from user.

    Child
    -----
    * textinput - contains text message.
    * sendbtn - sends the message.
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.textinput = TextInput(
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
            font=tkfont.Font(
                family="Roboto",
                size=16,
                weight="normal",
            ),
        )
        self.sendbtn = Button(
            self,
            text="send",
            bg="#096ad9",
            fg="#ffffff",
            font=tkfont.Font(family="Roboto", size=12, weight="normal"),
        )

        self.textinput.grid(row=0, column=0, sticky="nsew")
        self.sendbtn.grid(row=0, column=1, sticky="nse")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=self.sendbtn.winfo_width())

    def clear(self):
        """Cleans the text content."""
        self.textinput.delete("0", "end")
