"""
This module provides custom button widget.
"""

import tkinter as tk
from typing import Any

from .custom import CustomWidget
from .typing import (TkBtnCmd, TkBtnStateOpts, TkPosOpts, TkReliefOpts, TkScreenUnits,
    TkCursor, TkNone)


class Button(tk.Button, CustomWidget):
    """Custom button widget."""

    def __init__(self,
        master: tk.Misc,
        *,
        bitmap: tk.BitmapImage | TkNone = "",
        border: TkScreenUnits = 1,
        borderwidth: TkScreenUnits = 0,
        command: TkBtnCmd | TkNone = "",
        cursor: TkCursor = "",
        height: TkScreenUnits = 0,
        highlightthickness: TkScreenUnits = 0,
        image: tk.PhotoImage | TkNone = "",
        position: TkPosOpts = "none",
        padx: TkScreenUnits = 0,
        pady: TkScreenUnits = 0,
        relief: TkReliefOpts = "raised",
        state: TkBtnStateOpts = "normal",
        text: Any = "",
        variable: tk.Variable | TkNone = "",
        width: TkScreenUnits = 0,
        wraplength: TkScreenUnits = 0,
    ):
        """Arguments:

        * master - parent widget
        * bitmap - bitmap image name or path (with '@' prefix)
        * command - onclick callback
        * cursor - cursor appearance on hover
        * height/width - dimensions of widget
        * image - image
        * position - position of image w.r.t. text
        * padx/pady - horizontal/vertical padding
        * relief - button surface appearance
        * state - state of the button
        * text - button text
        * variable - tkinter variable
        """
        tk.Button.__init__(self, master=master, anchor="center", bd=0, bitmap=bitmap,
        border=border, borderwidth=borderwidth, command=command, compound=position,
        cursor=cursor, default=state, height=height,
        highlightthickness=highlightthickness, image=image, justify="center",
        overrelief="", padx=padx, pady=pady, relief=relief, state=state, text=text,
        textvariable=variable, underline=-1, width=width, wraplength=wraplength)
        CustomWidget.__init__(self)
