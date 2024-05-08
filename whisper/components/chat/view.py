from typing import Any, Dict
from whisper.components.base import TextBox


class View(TextBox):
    """A view for chat. Contains the chat messages.

    Methods
    -------
    * show_message - shows the message by the user on the chat.
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, cnf=self._cnf, **kwargs)

    def format(self, user: str, message: str) -> str:
        """Describes the format of the message to display on chat box."""
        return f"{user}: {message}\n"

    def __enter__(self):
        """A context manager to write into the view."""
        self.config(state="normal")
        return self

    def __exit__(self, *args, **kwargs):
        """Disable the view."""
        self.config(state="disabled")

    def show_message(self, user: str, message: str):
        """Displays the message sent by some user in the chat."""
        with self:
            self.insert("end", self.format(user.capitalize(), message))
        self.scroll_to_end()

    def show_info(self, info: str):
        """Displays the message sent by the server to the chat."""
        with self:
            self.insert("end", self.format("INFO", info))
        self.scroll_to_end()

    def scroll_to_end(self, force: bool = False):
        """Scroll to bottom of the chat."""
        if self.yview()[1] == 1.0 or force:
            self.yview_moveto(1.0)

    @property
    def _cnf(self) -> Dict[str, Any]:
        return {
            "state": "disabled",
            "bg": "#343145",
            "fg": "#ffffff",
            "font": ("Poppins", 12, "normal"),
        }
