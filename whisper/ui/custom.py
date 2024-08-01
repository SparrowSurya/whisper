import sys
import tkinter as tk
from typing import Callable, Tuple

from whisper.settings import MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, TITLEBAR_HEIGHT
from .widgets import Frame
from .titlebar import Titlebar


class CustomWindowMixin:
    """
    The class adds functionality to remove the default decoration on the
    tkinter window. This may not be reversed.
    """

    def __init__(self):
        self._is_customized = False

    @property
    def is_customized(self) -> bool:
        """Informs whethere window is customized or not."""
        return self._is_customized

    def mark_uncustomized(self):
        """Marks the internal variable uncustomized."""
        self._is_customized = False

    if sys.platform == "win32":

        def remove_default(self):
            """Remove default decoration on win32 platform."""
            self.overrideredirect(1)
            self.update_idletasks()
            self.withdraw()
            self._customize()

        def _customize(self):
            """Window hwnd related setting."""
            if not self.is_customized:
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
                self._is_customized = True

    else:

        def remove_default(self):
            """Remove default decoration on unsupported function. Raises `Exception`."""
            self._is_customized = False
            raise Exception("unable to customize")


class CustomWindowTitlebarMixin(CustomWindowMixin):
    """
    The class provides a custom titlebar and other functionality of
    default window decoration.
    """

    def __init__(self):
        super().__init__()
        self.__maximized = False
        self.__geometry = []
        self.__fullscreen = False
        self.__minsize = None

        self.remove_default()
        self.setup_widgets()

    def remove_default(self):
        """Remove default decoration if supported."""
        try:
            super().remove_default()
        except Exception:
            pass
        else:
            self.bind("<Map>", lambda _: self.minimize_reverse())
            self.title = self._title

    def setup_widgets(self):
        """Creates the widgets on the window."""
        self.root = self.get_root()
        if not self.is_customized:
            self.root.pack(fill="both", expand=1)
            return

        self.titlebar = Titlebar(self, height=TITLEBAR_HEIGHT)
        self.grip_n = Frame(self, cursor="top_side")
        self.grip_s = Frame(self, cursor="bottom_side")
        self.grip_e = Frame(self, cursor="right_side")
        self.grip_w = Frame(self, cursor="left_side")
        self.grip_ne = Frame(self, cursor="top_right_corner")
        self.grip_nw = Frame(self, cursor="top_left_corner")
        self.grip_se = Frame(self, cursor="bottom_right_corner")
        self.grip_sw = Frame(self, cursor="bottom_left_corner")

        self.grip_nw.grid(row=0, column=0, sticky="nsew")
        self.grip_n.grid(row=0, column=1, sticky="nsew")
        self.grip_ne.grid(row=0, column=2, sticky="nsew")

        self.grip_w.grid(row=1, column=0, sticky="nsew", rowspan=2)
        self.titlebar.grid(row=1, column=1, sticky="nsew")
        self.grip_e.grid(row=1, column=2, sticky="nsew", rowspan=2)

        self.root.grid(row=2, column=1, sticky="nsew")

        self.grip_sw.grid(row=3, column=0, sticky="nsew")
        self.grip_s.grid(row=3, column=1, sticky="nsew")
        self.grip_se.grid(row=3, column=2, sticky="nsew")

        self.grid_rowconfigure((0, 3), minsize=2, weight=0)
        self.grid_columnconfigure((0, 2), minsize=2, weight=0)
        self.grid_rowconfigure(1, minsize=TITLEBAR_HEIGHT)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grip_n.bind("<Button-1>", lambda e: self.resize("n", e))
        self.grip_s.bind("<Button-1>", lambda e: self.resize("s", e))
        self.grip_e.bind("<Button-1>", lambda e: self.resize("e", e))
        self.grip_w.bind("<Button-1>", lambda e: self.resize("w", e))
        self.grip_ne.bind("<Button-1>", lambda e: self.resize("ne", e))
        self.grip_nw.bind("<Button-1>", lambda e: self.resize("nw", e))
        self.grip_se.bind("<Button-1>", lambda e: self.resize("se", e))
        self.grip_sw.bind("<Button-1>", lambda e: self.resize("sw", e))

        self.titlebar.close.config(command=self.destroy)
        self.titlebar.maximize.config(command=self.toggle_maximize)
        self.titlebar.minimize.config(command=self.minimize)

        self.titlebar.bind("<Button-1>", self.move)
        self.titlebar.title.bind("<Button-1>", self.move)
        self.titlebar.icon.bind("<Button-1>", self.move)

        self.titlebar.title.bind(
            "<Double-Button-1>",
            lambda _: self.toggle_maximize(),
        )
        self.bind("<F11>", lambda _: self.toggle_fullscreen(), "+")
        self.on_close(self.destroy)

    def _title(self, title: str | None = None) -> None | str:
        """Set or get title on titlebar. Use this instead `wm_title`.
        If title is `None` then current title if returned."""
        if title is None:
            return self.titlebar.get_title()
        self.titlebar.set_title(title)

    @property
    def is_maximized(self) -> bool:
        """window maximized state."""
        return self.__maximized

    def toggle_maximize(self):
        """Maximize or Restore down functionality."""
        if self.is_maximized:
            self.restore_down()
        else:
            self.maximize()

    def maximize(self):
        """Maximize window. Hides the grip using geometry."""
        self.__geometry.append(self.winfo_geometry())
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.wm_geometry(f"{width+4}x{height+4}+{-2}+{-2}")
        self.__maximized = True
        self.titlebar.set_restore_down()

    def restore_down(self):
        """Restore down the window."""
        self.wm_geometry(self.__geometry.pop())
        self.__maximized = False
        self.titlebar.set_maximize()

    def minimize(self):
        """Minimize the window."""
        self.update_idletasks()
        self.overrideredirect(0)
        self.state("iconic")
        self.mark_uncustomized()

    def minimize_reverse(self):
        """Opposite of minize window."""
        self.overrideredirect(1)
        self.update_idletasks()
        self._customize()
        self.state("normal")

    def move(self, event: tk.Event):
        """Move the window."""
        x, y = self.winfo_x() - event.x_root, self.winfo_y() - event.y_root
        event.widget.bind(
            "<B1-Motion>",
            lambda e: self.wm_geometry(f"+{e.x_root + x}+{e.y_root + y}"),
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
            self.geometry(
                width + 4, height + titlebar_height + 4, -2, -2 - titlebar_height
            )
            self.__fullscreen = True

    def resize(self, anchor: str, event: tk.Event):
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

            width = nx2 - nx1
            height = ny2 - ny1

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
        if min_w not in range(1, self.winfo_screenwodth()) or min_h not in range(
            1, self.winfo_screenheight()
        ):
            raise ValueError(
                f"Inappropriate minimum width and height, got {min_w, min_h}"
            )
        self.__minsize = min_w, min_h

    # do not overwrite `protocol` method as it works different
    def on_close(self, callback: Callable[[], None]):
        """Callback when user clicks close button."""
        if self.is_customized:
            self.titlebar.close.config(command=callback)
        else:
            self.wm_protocol("WM_DELETE_WINDOW", callback)

    def get_root(self, parent: tk.Misc | None = None) -> tk.Widget:
        """Create root element of the window. All child must contained inside it."""
        if hasattr(self, "root"):
            return self.root
        return Frame(parent or self)

    def geometry(
        self,
        width: int,
        height: int,
        x: int | None = None,
        y: int | None = None,
        *,
        center: bool = False,
    ):
        """Configure dimensions and position of window.

        Arguments:
        * width, height - window dimensions.
        * x, y - window position.
        * center - ignores x, y and places it in screen center.
        """
        if center:
            x = int((self.winfo_screenwidth() / 2) - (width / 2))
            y = int((self.winfo_screenheight() / 2) - (height / 2))
        else:
            x = x if x is not None else self.winfo_x()
            y = y if y is not None else self.winfo_y()

        self.wm_geometry(f"{width}x{height}+{x}+{y}")


class CustomTkWindow(CustomWindowTitlebarMixin, tk.Tk):
    """
    Custom tkinter window with custom titlebar and all the previous
    functionality.
    """

    def __init__(self):
        tk.Tk.__init__(self)
        CustomWindowTitlebarMixin.__init__(self)


class CustomToplevelWindow(CustomWindowTitlebarMixin, tk.Toplevel):
    """
    Custom tkinter toplevel window with custom titlebar and all the previous
    functionality.
    """

    def __init__(self):
        tk.Toplevel.__init__(self)
        CustomWindowTitlebarMixin.__init__(self)
