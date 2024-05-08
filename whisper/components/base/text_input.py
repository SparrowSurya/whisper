import tkinter as tk


class TextInput(tk.Entry):
    """Custom base single line text widget."""


class TextBox(tk.Text):
    """Custom base multiline text widget."""

    # NOTE - does not work when the text still goes out of widget width
    def configure_height(self, limit: int, event=None):
        """Configure the height of widget as the text updates."""
        height = int(self.index("end - 1c").split(".")[0])
        self.config(height=min(height, limit))
