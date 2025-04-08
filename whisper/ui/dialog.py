"""
This module provides dialogue window widget.
"""

import tkinter as tk

from .custom import CustomWidget


class Dialog(tk.Toplevel, CustomWidget):
    """
    Tkinter dialog window. It allows window to show, hide and close. Initially
    window is hidden. `setup` is provided for child class to setup widgets and
    other configurations.
    """

    def __init__(self, master: tk.Misc):
        """Must provide master window."""
        tk.Toplevel.__init__(self, master)
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        CustomWidget.__init__(self)
        self.setup()

    def setup(self):
        """Setup widgets and other configurations."""

    def show(self):
        """Shows the dialogue window."""
        self.deiconify()
        self.lift()
        self.focus_set()
        self.grab_set()

    def hide(self):
        """Hides the dialogue window."""
        self.grab_release()
        self.withdraw()

    def close(self):
        """Close the dialogue window."""
        self.grab_release()
        self.destroy()

    def destroy(self):
        """Destroy the window and its children."""
        self.master.focus_set()
        self.master.focus()
        super().destroy()
