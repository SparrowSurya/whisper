import tkinter as tk

from ..theme import ThemeMixin

class Button(tk.Button, ThemeMixin):
    """Custom button widget."""