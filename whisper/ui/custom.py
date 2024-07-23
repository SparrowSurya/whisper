import sys
import tkinter as tk
from typing import Tuple

from whisper.settings import MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from .widgets import Frame


class CustomWindowMixin:
    """
    The mixin class provides customised window for the `tkinter.Tk` and
    `tkinter.Toplevel`. Supports `win32` platforms only but compatible
    with other platforms.

    NOTE:
    * tKinter window must be initialised.
    * this does not override `Wm` attributes.
    * all child widgets are subclass of `ThemeMixin`

    Children:
    * titlebar - custom titlebar for window.
    * borders - n, s, e, w, ne, nw, se, sw.
    * root - root element that should contain the child widgets.

    Usage:
    >>> class MyWindow(CustomWindowMixin, tkinter.Tk):
    >>>     def __init__(self, title: str, *args, customize=True, **kwargs):
    >>>         tkinter.Tk.__init__(self, *args, **kwargs)
    >>>         CustomWindowMixin.__init__(self, title, customize)
    """

    def __init__(self, title: str, customize: bool = True):
        """Creates customized window with given title."""

        self.root = Frame(self)
        """All child widgets must contains inside this."""

        if customize and sys.platform == "win32":
            self.setup_customization()
        else:
            self.root.pack(fill="both", expand=1)

        self.title(title)

    if sys.platform == "win32":

        def setup_customization(self):
            """Initialises the customization of window."""
            self.__maximized = False
            self.__geometry = []
            self.__customized = False
            self.__fullscreen = False
            self.__minsize = None

            self.bind("<Map>", lambda _: self.minimize_reverse())
            self.overrideredirect(1)
            self.__setup_widgets()
            self.update_idletasks()
            self.withdraw()
            self.__customize()
            self.__customized = True

            # tkinter Toplevel tries to get and set title during init
            self.title = self._title

            self.hide_minimize = self.titlebar.hide_minimize
            self.hide_maximize = self.titlebar.hide_maximize

        def __setup_widgets(self):
            """Creates custom widgets with the default window features."""
            from whisper.settings import TITLEBAR_HEIGHT
            from .titlebar import TitleBar

            # window titlebar
            self.titlebar = TitleBar(self, height=TITLEBAR_HEIGHT)

            # window resizing grips
            self.n = Frame(self, cursor="top_side")
            self.s = Frame(self, cursor="bottom_side")
            self.e = Frame(self, cursor="right_side")
            self.w = Frame(self, cursor="left_side")
            self.ne = Frame(self, cursor="top_right_corner")
            self.nw = Frame(self, cursor="top_left_corner")
            self.se = Frame(self, cursor="bottom_right_corner")
            self.sw = Frame(self, cursor="bottom_left_corner")

            self.nw.grid(row=0, column=0, sticky="nsew")
            self.n.grid(row=0, column=1, sticky="nsew")
            self.ne.grid(row=0, column=2, sticky="nsew")

            self.w.grid(row=1, column=0, sticky="nsew", rowspan=2)
            self.titlebar.grid(row=1, column=1, sticky="nsew")
            self.e.grid(row=1, column=2, sticky="nsew", rowspan=2)

            self.root.grid(row=2, column=1, sticky="nsew")

            self.sw.grid(row=3, column=0, sticky="nsew")
            self.s.grid(row=3, column=1, sticky="nsew")
            self.se.grid(row=3, column=2, sticky="nsew")

            self.grid_rowconfigure((0,3), minsize=2, weight=0)
            self.grid_columnconfigure((0,2), minsize=2, weight=0)
            self.grid_rowconfigure(1, minsize=TITLEBAR_HEIGHT)
            self.grid_rowconfigure(2, weight=1)
            self.grid_columnconfigure(1, weight=1)

            self.n.bind("<Button-1>", lambda e: self._resize("n", e))
            self.s.bind("<Button-1>", lambda e: self._resize("s", e))
            self.e.bind("<Button-1>", lambda e: self._resize("e", e))
            self.w.bind("<Button-1>", lambda e: self._resize("w", e))
            self.ne.bind("<Button-1>", lambda e: self._resize("ne", e))
            self.nw.bind("<Button-1>", lambda e: self._resize("nw", e))
            self.se.bind("<Button-1>", lambda e: self._resize("se", e))
            self.sw.bind("<Button-1>", lambda e: self._resize("sw", e))

            self.titlebar.close.config(command=self.destroy)
            self.titlebar.maximize.config(command=self.toggle_maximize)
            self.titlebar.minimize.config(command=self.minimize)

            self.titlebar.bind("<Button-1>", self._move)
            self.titlebar.title.bind("<Button-1>", self._move)
            self.titlebar.icon.bind("<Button-1>", self._move)

            self.titlebar.title.bind(
                    "<Double-Button-1>",
                    lambda _: self.toggle_maximize(),
            )
            self.bind("<F11>", lambda _: self.toggle_fullscreen())

        def _title(self, title: str | None = None) -> None | str:
            """Set title on titlebar. Use this instead `wm_title`.
            If title is `None` then current title if returned."""
            # tkinter.Toplevel gets and sets title before actual titlebar is created
            if title is None:
                return self.titlebar.get_title()
            self.titlebar.set_title(title)

        def __customize(self):
            """Configure windows window setting."""
            if not self.__customized:
                from ctypes import windll

                GWL_EXSTYLE = -20
                WS_EX_APPWINDOW = 0x00040000
                WS_EX_TOOLWINDOW = 0x00000080

                hwnd = windll.user32.GetParent(self.winfo_id())
                style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                style = style & ~WS_EX_TOOLWINDOW
                style = style | WS_EX_APPWINDOW
                windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
                self.withdraw()
                self.wm_deiconify()
                self.__customized = True

        @property
        def is_maximized(self) -> bool:
            """window maximized state."""
            return self.__maximized

        def toggle_maximize(self):
            """Maximize or Restore down functionality."""
            if self.is_maximized:
                self._restore_down()
            else:
                self._maximize()

        def _maximize(self):
            """Maximize window. Hides the grip using geometry."""
            self.__geometry.append(self.winfo_geometry())
            width, height = self.winfo_screenwidth(), self.winfo_screenheight()
            self.wm_geometry(f"{width-4}x{height-5}+{-2}+{-2}")
            self.__maximized = True
            self.titlebar.set_restore_down()

        def _restore_down(self):
            """Restore down the window."""
            self.wm_geometry(self.__geometry.pop())
            self.__maximized = False
            self.titlebar.set_maximize()

        def minimize(self):
            """Minimize the window."""
            self.update_idletasks()
            self.overrideredirect(0)
            self.state("iconic")
            self.__customized = False

        def minimize_reverse(self):
            """Opposite of minize window."""
            self.overrideredirect(1)
            self.update_idletasks()
            self.__customize()
            self.state("normal")

        def _move(self, event: tk.Event):
            """Move the window."""
            x, y = self.winfo_x() - event.x_root, self.winfo_y() - event.y_root
            event.widget.bind(
                "<B1-Motion>",
                lambda e: self.wm_geometry(f"+{e.x_root + x}+{e.y_root + y}"),
                "", # override previous callback
            )

        @property
        def is_fullscreen(self) -> bool:
            """Window fullscreen state."""
            return self.__fullscreen

        def toggle_fullscreen(self):
            """Toggle fullscreen on/off."""
            if self.is_fullscreen:
                self.wm_geometry(self.__geometry.pop())
                self.__fullscreen = False
            else:
                self.__geometry.append(self.winfo_geometry())
                titlebar_height = self.titlebar.winfo_height()
                width, height = self.winfo_screenwidth(), self.winfo_screenheight()
                self.geometry(width+4, height+titlebar_height+4, -2, -2-titlebar_height)
                self.__fullscreen = True

        def _resize(self, anchor: str, event: tk.Event):
            """Manually resize the window."""
            ex, ey = event.x_root, event.y_root

            x1 = self.winfo_x()
            y1 = self.winfo_y()
            x2 = x1 + self.winfo_width()
            y2 = y1 + self.winfo_height()

            if self.__minsize:
                min_width, min_height = self.minsize
            else:
                min_width = MIN_WINDOW_WIDTH
                min_height = MIN_WINDOW_HEIGHT

            def resize(e: tk.Event):
                nonlocal min_width, min_height

                dx = e.x_root - ex
                dy = e.y_root - ey

                ny1 = y1 + (dy if "n" in anchor else 0)
                ny1 = ny1 if ny1 < y2 else y2

                ny2 = y2 + (dy if "s" in anchor else 0)
                ny2 = ny2 if ny2 > y1 else y1

                nx2 = x2 + (dx if "e" in anchor else 0)
                nx2 = nx2 if nx2 > x1 else x1

                nx1 = x1 + (dx if "w" in anchor else 0)
                nx1 = nx1 if nx1 < x2 else x2

                width = nx2-nx1
                height = ny2-ny1

                if width < min_width:
                    if "w" in anchor:
                        nx1 -= min_width - width
                    if "e" in anchor:
                        nx2 += min_width - width
                    width = min_width

                if height < min_height:
                    if "n" in anchor:
                        ny1 -= min_height - height
                    if "s" in anchor:
                        ny2 += min_height - height
                    height = min_height

                self.wm_geometry(f"{width}x{height}+{nx1}+{ny1}")

            event.widget.bind("<B1-Motion>", resize, "")

        @property
        def minsize(self) -> Tuple[int, int]:
            """Minimum allowed size of the window."""
            return self.__minsize or (MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        def set_minsize(self, min_w: int, min_h: int):
            """Set minimum width and height of the window."""
            if (
                min_w not in range(1, self.winfo_screenwodth())
                or min_h not in range(1, self.winfo_screenheight())
            ):
                raise ValueError(f"Inappropriate minimum width and height, got {min_w, min_h}")
            self.__minsize = min_w, min_h


    def geometry(self, width: int, height: int, x: int | None = None, y: int | None = None, *, center: bool = False):
        """Configure dimensions and position of window.

        Arguments:
        * width, height - window dimensions.
        * x, y - window position.
        * center - ignores x, y and places it in screen center.
        """
        if center:
            x = int((self.winfo_screenwidth()/2) - (width/2))
            y = int((self.winfo_screenheight()/2) - (height/2))
        else:
            x = x if x is not None else self.winfo_x()
            y = y if y is not None else self.winfo_y()

        self.wm_geometry(f"{width}x{height}+{x}+{y}")


def main():
    """A simple demonstration."""

    class MyToplevel(CustomWindowMixin, tk.Toplevel):
        def __init__(self, title: str, *args, customize: bool = True, **kwargs):
            tk.Toplevel.__init__(self, *args, **kwargs)
            CustomWindowMixin.__init__(self, title, customize)

            self.name = tk.Label(self.root, text="Yay!")
            self.name.pack()


    class MyWindow(CustomWindowMixin, tk.Tk):
        def __init__(self, title: str, *args, customize: bool = True, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            CustomWindowMixin.__init__(self, title, customize)

            self.toplevel = None

            self.name = tk.Entry(self.root)
            self.name.pack()

            self.show = tk.Button(self.root, text="Toplevel")
            self.show.pack()
            self.show.config(command=self.show_toplevel)

        def show_toplevel(self):
            try:
                self.toplevel.destroy()
            except (AttributeError, tk.TclError):
                pass
            finally:
                self.toplevel = MyToplevel(self.name.get().strip() or "Toplevel")
                self.name.delete("0", "end")


    win = MyWindow("MyWindow")
    win.mainloop()


if __name__ == "__main__":
    main()
