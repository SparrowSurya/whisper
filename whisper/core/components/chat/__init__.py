from whisper.core.components.base.container import Container
from whisper.core.components.base.label import Label
from whisper.core.components.base.button import Button
from whisper.core.components.base.text_input import TextBox, TextInput


class ChatBox(Container):
    """Manages the chatting for user."""

    _username = "Unknown"

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.title = Label(self, text=self._username)
        self.chat = TextBox(self, state="disabled", wrap="word")
        self.textinput = TextInput(self)
        self.sendbtn = Button(self, text="Send")

        self.title.grid(row=0, column=0, sticky="new", columnspan=2)
        self.chat.grid(row=1, column=0, sticky="nsew", columnspan=2)
        self.textinput.grid(row=2, column=0, sticky="nsew")
        self.sendbtn.grid(row=2, column=1, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=self.sendbtn.winfo_width())

        self.sendbtn.config(command=self.on_send)
        self.textinput.bind("<Return>", self.on_send)
        self.textinput.focus()

    def on_send(self, event=None):
        """Event listener on the send button."""
        if msg := self.textinput.get().strip():
            self.send_message(msg)
            self.textinput.delete("0", "end")

    def set_username(self, name: str):
        """Sets the username on the chat."""
        self._username = name
        self.title.config(text=self._username)

    def format(self, user: str, message: str, end: str = "\n") -> str:
        """Describes the format of the message to display on chat box."""
        return f"{user.capitalize()}: {message}{end}"

    def show_message(self, user: str, message: str):
        """Displays the message in the chat box."""
        self.chat.config(state="normal")
        self.chat.insert("end", self.format(user, message))
        self.chat.config(state="disabled")

    def send_message(self, message: str):
        """Sends the message."""
        self.show_message(self._username, message)
