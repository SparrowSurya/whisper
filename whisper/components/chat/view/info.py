from typing import Any, Dict
from whisper.components.base import Container, Label


class Info(Container):
    """Text Message in the chat."""

    def __init__(self, master, *args, info: str, **kwargs):
        super().__init__(master, *args, cnf=self._cnf, **kwargs)

        self.body = Label(
            self,
            text=info,
            bg="#343145",
            fg="#656881",
            justify="center",
            anchor="center",
            font=("Roboto", 14, "normal"),
        )
        self.body.pack(fill="x", anchor="center")

    @property
    def _cnf(self) -> Dict[str, Any]:
        return {
            "bg": "#343145",
        }
