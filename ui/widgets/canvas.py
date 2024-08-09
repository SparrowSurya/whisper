import tkinter as tk

from ..theme import ThemeMixin


class Canvas(tk.Canvas, ThemeMixin):
    """Custom canvas widget."""