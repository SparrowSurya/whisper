import tkinter as tk

from .widgets import Label, Frame, Button


class Titlebar(Frame):
    """Custom Titlebar widget.

    Child widgets: icon, title, minimize, maximize, close.

    NOTE - The parent of this widget must be instance of `tkinter.Tk`
    or `tkinter.Toplevel`.
    """

    __theme_attrs__ = {
        "background": "surfaceContainerLowest",
    }

    def __init__(self, master, *args, height: int, **kwargs):
        """Height is a required parameter of the widget."""
        super().__init__(master, *args, height=height, **kwargs)

        self.icon_image = tk.PhotoImage()
        self.blank_img = tk.PhotoImage()

        self.icon = Label(
            self,
            image=self.icon_image,
            compound="center",
            width=height,
            height=height,
        )
        self.title = Label(
            self,
            text="",
            image=self.blank_img,
            compound="center",
            font=("Roboto", 12, "normal"),
            justify="left",
            anchor="w",
            height=height,
        )
        self.minimize = Button(
            self,
            text="",
            image=self.blank_img,
            compound="center",
            font=("Roboto", 14, "bold"),
            relief="flat",
            width=28,
            padx=8,
            highlightthickness=0,
            border=0,
            borderwidth=0,
            height=height,
        )
        self.maximize = Button(
            self,
            text="",
            image=self.blank_img,
            compound="center",
            font=("Roboto", 14, "bold"),
            relief="flat",
            width=28,
            padx=8,
            highlightthickness=0,
            border=0,
            borderwidth=0,
            height=height,
        ) # "" Restore Down, "" maximize
        self.close = Button(
            self,
            text="",
            image=self.blank_img,
            compound="center",
            font=("Roboto", 14, "bold"),
            relief="flat",
            width=28,
            padx=8,
            highlightthickness=0,
            border=0,
            borderwidth=0,
            height=height,
        )

        self.icon.grid(row=0, column=0, sticky="nsew", padx=4, pady=0)
        self.title.grid(row=0,column=1, sticky="nsew", padx=0, pady=0)
        self.minimize.grid(row=0, column=2, sticky="nsew", padx=0, pady=0)
        self.maximize.grid(row=0, column=3, sticky="nsew", padx=0, pady=0)
        self.close.grid(row=0, column=4, sticky="nsew", padx=0, pady=0)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0,2,3,4), minsize=height)
        self.grid_rowconfigure(0, minsize=height)

    def set_title(self, title: str):
        """Set title on titlebar."""
        self.title.config(text=title)

    def get_title(self) -> str:
        """Get title on titlebar."""
        return self.title.cget("text")

    def set_icon(self, file: str | bytes):
        """set icon on titlebar."""
        self.icon_image = tk.PhotoImage(file=file)
        self.icon.config(image=self.icon_image)

    def set_restore_down(self):
        """Set the restore down glyph instead maximize."""
        self.maximize.config(text="")

    def set_maximize(self):
        """Set the maximize glyph instead restore down."""
        self.maximize.config(text="")

    def hide_minimize(self):
        """Hide minimize button in titlebar."""
        self.minimize.grid_remove()
        self.grid_columnconfigure(2, minsize=0)

    def hide_maximize(self):
        """Hide maximize toggle button."""
        self.maximize.grid_remove()
        self.grid_columnconfigure(3, minsize=0)
