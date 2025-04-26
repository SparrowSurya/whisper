"""
This module provides custom container widget.
"""

import tkinter as tk
from typing import Mapping

from .custom import CustomWidget
from whisper.typing import (
    Cursor as _Cursor,
    ScreenUnit as _ScreenUnit,
    Relief as _Relief,
    ContainerColorAttr as _ColorAttr,
    PaletteOpts as _PaletteOpts,
    Misc as _Misc,
)


class Container(tk.Frame, CustomWidget):
    """Custom container widget."""

    def __init__(self,
        master: _Misc,
        *,
        border: _ScreenUnit = 0,
        borderwidth: _ScreenUnit = 0,
        cursor: _Cursor = "",
        container: bool = False,
        height: _ScreenUnit = 0,
        highlightthickness: _ScreenUnit = 0,
        padx: _ScreenUnit = 0,
        pady: _ScreenUnit = 0,
        relief: _Relief = "flat",
        width: _ScreenUnit = 0,
    ):
        tk.Frame.__init__(self, master=master, border=border, borderwidth=borderwidth,
            cursor=cursor, container=container, height=height,
            highlightthickness=highlightthickness, padx=padx, pady=pady, relief=relief,
            width=width)
        CustomWidget.__init__(self)

    @classmethod
    def default_colorscheme(cls) -> Mapping[_ColorAttr, _PaletteOpts]:
        """Default colorscheme for container widget."""
        return {
            "background": "mantle",
            "highlightbackground": "surface0",
            "highlightcolor": "accent",
        }
