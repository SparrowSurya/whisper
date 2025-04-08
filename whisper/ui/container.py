"""
This module provides custom container widget.
"""

import tkinter as tk

from .custom import CustomWidget
from .typing import TkCursor, TkReliefOpts, TkScreenUnits


class Container(tk.Frame, CustomWidget):
    """Custom container widget."""

    def __init__(self,
        master: tk.Misc,
        *,
        border: TkScreenUnits = 0,
        borderwidth: TkScreenUnits = 0,
        cursor: TkCursor = "",
        height: TkScreenUnits = 0,
        highlightthickness: TkScreenUnits = 0,
        padx: TkScreenUnits = 0,
        pady: TkScreenUnits = 0,
        relief: TkReliefOpts = "flat",
        width: TkScreenUnits = 0,
    ):
        tk.Frame.__init__(self, master=master, border=border, borderwidth=borderwidth,
            cursor=cursor, height=height, highlightthickness=highlightthickness,
            padx=padx, pady=pady, relief=relief, width=width)
        CustomWidget.__init__(self)
