"""
This module provides custom label widget.
"""

import tkinter as tk
from typing import Mapping

from .custom import CustomWidget
from whisper.typing import (
    LabelJustify as _LabelJustify,
    Relief as _Relief,
    ScreenUnit as _ScreenUnit,
    Cursor as _Cursor,
    Compound as _Compound,
    LabelColorAttr as _ColorAttr,
    PaletteOpts as _PaletteOpts,
    Bitmap as _Bitmap,
    Variable as _Variable,
    Image as _Image,
    Misc as _Misc,
)


class Label(tk.Label, CustomWidget):
    """Custom label widget."""

    def __init__(self,
        master: _Misc,
        *,
        bitmap: _Bitmap = "",
        border: _ScreenUnit = 0,
        borderwidth: _ScreenUnit = 0,
        cursor: _Cursor = "",
        compound: _Compound = "none",
        height: _ScreenUnit = 0,
        highlightthickness: _ScreenUnit = 0,
        image: _Image = "",
        justify: _LabelJustify = "center",
        padx: _ScreenUnit = 0,
        pady: _ScreenUnit = 0,
        relief: _Relief = "flat",
        text: str = "",
        width: _ScreenUnit = 0,
        variable: _Variable = "",
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
