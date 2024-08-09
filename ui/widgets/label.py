import tkinter as tk

from ..theme import ThemeMixin


class Label(tk.Label, ThemeMixin):
    """Custom label widget."""