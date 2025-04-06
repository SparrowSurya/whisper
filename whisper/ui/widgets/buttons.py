"""
This module provides custom button widget.
"""

import tkinter as tk

from .custom import CustomWidget
from .typing import TkBtnCmd, TkBtnStateOpts, TkPosOpts, TkReliefOpts


class Button(tk.Button, CustomWidget):
    """Custom button widget."""

    def __init__(self,
        master: tk.Misc,
        *,
        bitmap: str = "",
        border: int = 1,
        borderwidth: int = 0,
        command: TkBtnCmd | None = None,
        cursor: str = "",
        height: int = 0,
        highlightthickness: int = 0,
        image: tk.PhotoImage | None = None,
        position: TkPosOpts = "none",
        padx: int = 0,
        pady: int = 0,
        relief: TkReliefOpts = "raised",
        state: TkBtnStateOpts = "normal",
        text: str = "",
        variable: tk.Variable | None = None,
        width: int = 0,
        wraplength: int = 0,
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
