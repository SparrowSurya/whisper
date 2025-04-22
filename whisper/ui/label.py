"""
This module provides custom label widget.
"""

import tkinter as tk
from typing import Mapping

from .custom import CustomWidget
from whisper.typing import (
    LabelJustify as _LabelJustify,
    Relief as _Relief,
    Empty as _Empty,
    ScreenUnit as _ScreenUnit,
    Cursor as _Cursor,
    Compound as _Compound,
    LabelColorAttr as _ColorAttr,
    PaletteOpts as _PaletteOpts,
)


class Label(tk.Label, CustomWidget):
    """Custom label widget."""

    def __init__(self,
        master: tk.Misc,
        *,
        bitmap: tk.BitmapImage | _Empty = "",
        border: _ScreenUnit = 0,
        borderwidth: _ScreenUnit = 0,
        cursor: _Cursor = "",
        compound: _Compound = "none",
        height: _ScreenUnit = 0,
        highlightthickness: _ScreenUnit = 0,
        image: tk.PhotoImage | _Empty = "",
        justify: _LabelJustify = "center",
        padx: _ScreenUnit = 0,
        pady: _ScreenUnit = 0,
        relief: _Relief = "flat",
        text: str = "",
        width: _ScreenUnit = 0,
        variable: tk.Variable | _Empty = "",
    ):
        tk.Label.__init__(self, master, anchor=justify, bitmap=bitmap, border=border,
            borderwidth=borderwidth, cursor=cursor, compound=compound, height=height,
            highlightthickness=highlightthickness, image=image, padx=padx, pady=pady,
            relief=relief, state="normal", takefocus=False, text=text,
            textvariable=variable, underline=-1, width=width, wraplength=0)
        CustomWidget.__init__(self)

    @classmethod
    def default_colorscheme(cls) -> Mapping[_ColorAttr, _PaletteOpts]:
        return {
            "background": "base",
            "foreground": "text",
            "highlightbackground": "surface0",
            "highlightcolor": "blue",
        }
