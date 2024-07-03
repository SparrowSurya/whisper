from typing import Any, Dict
from whisper.ui.widgets import Frame, Label


class Info(Frame):
    """Display the information in chat."""

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
        self.body.bind(
            "<Configure>",
            lambda e: self.body.configure(wraplength=self.body.master.winfo_width()),
            "+",
        )

    @property
    def _cnf(self) -> Dict[str, Any]:
        return {
            "bg": "#343145",
        }
