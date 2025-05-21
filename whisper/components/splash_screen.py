"""
This module provides the splash screen for the client application.
"""

import tkinter as tk

from whisper.ui import Window, Container, Button
from whisper.typing import Misc as _Misc



class SplashToolbar(Container):
    """Replacement for splash screen titlebar tool options."""

    def __init__(self, master: _Misc, **kwargs):
        Container.__init__(self, master, **kwargs)

        self.blank_img = tk.PhotoImage()

        self.close_btn = Button(self,
            text="",
            image=self.blank_img,
            compound="center",
            relief="flat",
            width=28,
            height=28,
            padx=8,
            highlightthickness=0,
            border=0,
            borderwidth=0,
            command=self.master.app.shutdown)
        self.minimize_btn = Button(self,
            text="",
            image=self.blank_img,
            compound="center",
            relief="flat",
            width=28,
            height=28,
            padx=8,
            highlightthickness=0,
            border=0,
            borderwidth=0)

        self.close_btn.pack(side="right")
        self.minimize_btn.pack(side="right")


    def setup(self):
        super().setup()
        self.close_btn.config(font=("Roboto", 14, "bold"))
        self.minimize_btn.config(font=("Roboto", 14, "bold"))


class SplashRoot(Container):
    """Body of the splash screen."""

    def __init__(self, master: _Misc, **kwargs):
        Container.__init__(self, master, **kwargs)
        self.app = master.app

        self.toolbar = SplashToolbar(self)
        self.toolbar.pack(fill="x")



class SplashWindow(Window):

    def __init__(self, master: _Misc):
        Window.__init__(self, master)
        self.app = master.app
        self.config(padx=1, pady=1)
        self.overrideredirect(True)

        self.root = SplashRoot(self, height=320, width=240)
        self.root.bind("<Button-1>", self.app.shutdown)

    def setup(self):
        super().setup()
        self.root.pack(fill="both", expand=1)
        self.root.setup()
        self.center_window(320, 240)
        self.app.hide_window()
        self.show_window()

    @classmethod
    def default_colorscheme(cls):
        return {
            **super().default_colorscheme(),
            "background": "accent",
        }
