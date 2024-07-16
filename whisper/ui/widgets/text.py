import tkinter as tk

from ..theme import ThemeMixin


class Text(tk.Text, ThemeMixin):
    """Custom text widget."""