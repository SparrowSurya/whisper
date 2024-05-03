import tkinter as tk


class Container(tk.Frame):
    """Custom base container widget."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)