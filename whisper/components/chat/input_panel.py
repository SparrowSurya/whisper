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

        self.textinput = TextInput(self)
        self.sendbtn = Button(self, text="send")

        self.textinput.grid(row=0, column=0, sticky="nsew")
        self.sendbtn.grid(row=0, column=1, sticky="nse")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=self.sendbtn.winfo_width())

    def clear(self):
        """Cleans the text content."""
        self.textinput.delete("0", "end")
