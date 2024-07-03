from typing import Dict, Any

from whisper.ui.widgets import Frame, Label


class TopBar(Frame):
    """
    Chat topbar which contains some userful things.

    Useful things:
    * title - display the title on chat.
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, cnf=self._cnf, **kwargs)

        self.title = Label(
            self,
            text="",
            justify="left",
            anchor="w",
            bg="#343145",
            fg="#ffffff",
            font=("Roboto", 14, "bold"),
        )
        self.title.pack(side="left", fill="x")

    def set_title(self, title: str):
        """Sets the title on header."""
        self.title.config(text=title)

    @property
    def _cnf(self) -> Dict[str, Any]:
        return {
            "bg": "#343145",
        }
