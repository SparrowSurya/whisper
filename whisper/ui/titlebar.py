import tkinter as tk

from .widgets import Label, Frame, Button
from whisper.settings import TITLEBAR_HEIGHT, DEFAULT_ICON_PATH


class TitleBar(Frame):
    """TitleBar for the custom window."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.icon_image = tk.PhotoImage(file=DEFAULT_ICON_PATH)
        self.blank_img = tk.PhotoImage()

        self.icon = Label(
            self,
            image=self.icon_image,
            compound="center",
            width=TITLEBAR_HEIGHT,
            height=TITLEBAR_HEIGHT,
        )
        self.title = Label(
            self,
            text="",
            image=self.blank_img,
            compound="center",
            font=("Open Sans", 14, "normal"),
            justify="left",
            anchor="w",
            height=TITLEBAR_HEIGHT,
        )
        self.minimize = Button(
            self,
            text="",
            image=self.blank_img,
            compound="center",
            font=("Roboto", 24, "bold"),
            relief="flat",
            width=32,
            height=TITLEBAR_HEIGHT,
            padx=8,
            highlightthickness=0,
            border=0,
            borderwidth=0,
        )
        self.maximize = Button(
            self,
            text="",
            image=self.blank_img,
            compound="center",
            font=("Roboto", 24, "bold"),
            relief="flat",
            width=32,
            height=TITLEBAR_HEIGHT,
            padx=8,
            highlightthickness=0,
            border=0,
            borderwidth=0,
        ) # "" Restore Down, "" maximize
        self.close = Button(
            self,
            text="",
            image=self.blank_img,
            compound="center",
            font=("Roboto", 24, "bold"),
            relief="flat",
            width=32,
            height=TITLEBAR_HEIGHT,
            padx=8,
            highlightthickness=0,
            border=0,
            borderwidth=0,
        )

        self.icon.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.title.grid(row=0,column=1, sticky="nsew", padx=0, pady=0)
        self.minimize.grid(row=0, column=2, sticky="nse", padx=0, pady=0)
        self.maximize.grid(row=0, column=3, sticky="nse", padx=0, pady=0)
        self.close.grid(row=0, column=4, sticky="nse", padx=0, pady=0)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0,2,3,4), minsize=45)
        self.grid_rowconfigure(0, minsize=TITLEBAR_HEIGHT)

    def set_title(self, title: str, justify: str = "left"):
        """Sets title on titlebar."""
        self.title.config(text=title, justify=justify)

    def get_title(self) -> str:
        """Get title on titlebar."""
        self.title.cget("text")

    def set_restore_down(self):
        """Sets the restore down glyph instead maximize."""
        self.maximize.config(text="")

    def set_maximize(self):
        """Sets the maximize glyph instead restore down."""
        self.maximize.config(text="")

    def hide_minimize(self):
        """Hide minimize button in titlebar."""
        self.minimize.grid_remove()
        self.grid_columnconfigure(2, minsize=0)

    def hide_maximize(self):
        """Hide maximize toggle button."""
        self.maximize.grid_remove()
        self.grid_columnconfigure(3, minsize=0)