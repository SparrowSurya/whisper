"""
This module provides custom container widget.
"""

import tkinter as tk

from .custom import CustomWidget
from .typing import TkReliefOpts


class Container(tk.Frame, CustomWidget):
    """Custom container widget."""

    def __init__(self,
        master: tk.Misc,
        *,
        border: int = 0,
        borderwidth: int = 0,
        cursor: str = "",
        height: int = 0,
        highlightthickness: int = 0,
        padx: int = 0,
        pady: int = 0,
        relief: TkReliefOpts = "flat",
        width: int = 0,
    ):
        tk.Frame.__init__(self, master=master, border=border, borderwidth=borderwidth,
            cursor=cursor, height=height, highlightthickness=highlightthickness,
            padx=padx, pady=pady, relief=relief, width=width)
        CustomWidget.__init__(self)
