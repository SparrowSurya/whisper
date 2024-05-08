from typing import Any, Dict
from whisper.components.base import Container, Label


class Message(Container):
    """Text Message in the chat."""

    def __init__(self, master, *args, username: str, message: str, **kwargs):
        super().__init__(master, *args, cnf=self._cnf, **kwargs)

        self.head = Label(
            self,
            text=username,
            bg="#343145",
            fg="#ff66b7",
            height=1,
            justify="left",
            anchor="nw",
            font=("Roboto", 14, "bold", "underline"),  # type: ignore
        )
        self.body = Label(
            self,
            text=message,
            bg="#343145",
            fg="#d7d7da",
            justify="left",
            anchor="nw",
            font=("Roboto", 14, "normal"),
        )

        self.head.pack(fill="x", anchor="nw")
        self.body.pack(fill="x", anchor="sw")

        self.body.bind("<Configure>", self.body.wraplength)

    @property
    def _cnf(self) -> Dict[str, Any]:
        return {
            "bg": "#343145",
        }
