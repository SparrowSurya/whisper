import tkinter as tk


class Label(tk.Label):
    """Custom base label widget."""

    def wraplength(self, event=None):
        """Event listener bindnded using `<Configure>` to enable automatic wrap by word."""
        self.config(wraplength=self.master.winfo_width())
