"""
This module provides custom button widget.
"""

import tkinter as tk
from typing import Mapping

from .custom import CustomWidget
from whisper.typing import (
    ScreenUnit as _ScreenUnit,
    Cursor as _Cursor,
    Relief as _Relief,
    ButtonState as _ButtonState,
    BUttonCmd as _ButtonCmd,
    Compound as _Compound,
    ButtonColorAttr as _ColorAttr,
    PaletteOpts as _PaletteOpts,
    Bitmap as _Bitmap,
    Image as _Image,
    Variable as _Variable,
    Misc as _Misc,
)


class Button(tk.Button, CustomWidget):
    """Custom button widget."""

    def __init__(self,
        master: _Misc,
        *,
        bitmap: _Bitmap = "",
        border: _ScreenUnit = 1,
        borderwidth: _ScreenUnit = 0,
        command: _ButtonCmd = "",
        compound: _Compound = "none",
        cursor: _Cursor = "",
        height: _ScreenUnit = 0,
        highlightthickness: _ScreenUnit = 0,
        image: _Image = "",
        padx: _ScreenUnit = 0,
        pady: _ScreenUnit = 0,
        relief: _Relief = "raised",
        state: _ButtonState = "normal",
        text: str = "",
        variable: _Variable = "",
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

    @classmethod
    def default_colorscheme(cls) -> Mapping[_ColorAttr, _PaletteOpts]:
        return {
            "background": "surface0",
            "foreground": "text",
            "activebackground": "surface1",
            "activeforeground": "text",
            "disabledforeground": "overlay1",
            "highlightbackground": "surface1",
            "highlightcolor": "blue",
        }
