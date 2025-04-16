"""
This module provides custom button widget.
"""

import tkinter as tk

from .custom import CustomWidget
from whisper.typing import (
    ScreenUnit as _ScreenUnit,
    Empty as _Empty,
    Cursor as _Cursor,
    Relief as _Relief,
    ButtonState as _ButtonState,
    BUttonCmd as _ButtonCmd,
    Compound as _Compound,
)


class Button(tk.Button, CustomWidget):
    """Custom button widget."""

    def __init__(self,
        master: tk.Misc,
        *,
        bitmap: tk.BitmapImage | _Empty = "",
        border: _ScreenUnit = 1,
        borderwidth: _ScreenUnit = 0,
        command: _ButtonCmd | _Empty = "",
        compound: _Compound = "none",
        cursor: _Cursor = "",
        height: _ScreenUnit = 0,
        highlightthickness: _ScreenUnit = 0,
        image: tk.PhotoImage | _Empty = "",
        padx: _ScreenUnit = 0,
        pady: _ScreenUnit = 0,
        relief: _Relief = "raised",
        state: _ButtonState = "normal",
        text: str = "",
        variable: tk.Variable | _Empty = "",
        width: _ScreenUnit = 0,
        wraplength: _ScreenUnit = 0,
    ):
        tk.Button.__init__(self, master=master, anchor="center", bd=0, bitmap=bitmap,
        border=border, borderwidth=borderwidth, command=command, compound=compound,
        cursor=cursor, default=state, height=height,
        highlightthickness=highlightthickness, image=image, justify="center",
        overrelief="", padx=padx, pady=pady, relief=relief, state=state, text=text,
        textvariable=variable, underline=-1, width=width, wraplength=wraplength)
        CustomWidget.__init__(self)
