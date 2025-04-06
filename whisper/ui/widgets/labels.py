"""
This module provides custom label widget.
"""

import tkinter as tk

from .custom import CustomWidget
from .typing import TkJustifyOpts, TkReliefOpts, TkPosOpts


class Label(tk.Label, CustomWidget):
    """Custom label widget."""

    def __init__(self,
        master: tk.Misc,
        *,
        bitmap: str = "",
        border: int = 0,
        borderwidth: int = 0,
        cursor: str = "",
        height: int = 0,
        highlightthickness: int = 0,
        image: tk.PhotoImage | None = None,
        justify: TkJustifyOpts = "center",
        position: TkPosOpts = "none",
        padx: int = 0,
        pady: int = 0,
        relief: TkReliefOpts = "flat",
        text: str = "",
        width: int = 0,
        variable: tk.Variable | None = None,
    ):
        """Arguments:

        * master - parent tkinter widget
        * bitmap - bitmap image (for filepath use '@' prefix)
        * justify - text position (w: left, e: right)
        * position - position of image w.r.t text
        * padx/pady - horizontal/vertial padding
        * height/width - dimensions of widget
        * text - text displayed by widget
        * variable - tkinter variable
        """
        tk.Label.__init__(self, master, anchor=justify, bitmap=bitmap, border=border,
            borderwidth=borderwidth, cursor=cursor, compound=position, height=height,
            highlightthickness=highlightthickness, image=image, padx=padx, pady=pady,
            relief=relief, state="normal", takefocus=False, text=text,
            textvariable=variable, underline=-1, width=width, wraplength=0)
        CustomWidget.__init__(self)
