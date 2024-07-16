import sys
import tkinter as tk

from .canvas import Canvas
from .frame import Frame


class ScrollableFrame(Frame):
    """Custom scrollable frame."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._setup_scroll(*args, **kwargs)
        self._setup_theme()

    def _setup_scroll(self, *args, **kwargs):
        """Setup scroll on the container."""
        self._canvas = Canvas(self, highlightthickness=0, borderwidth=0)
        self._canvas.pack(fill="both", expand=1)

        self._frame = Frame(self._canvas, *args, **kwargs)
        self.fid = self._canvas.create_window(0, 0, anchor="nw", window=self._frame)

        self._frame.bind("<Configure>", self.configure_canvas)
        self._canvas.bind("<Configure>", self.configure_frame)

        if sys.platform == "win32":
            self._canvas.bind("<MouseWheel>", self._on_scroll)
            self.bind_class("scroll", "<MouseWheel>", self._on_scroll)
        elif sys.platform == "linux":
            self._canvas.bind("<Button-4>", self._on_scroll)
            self._canvas.bind("<Button-5>", self._on_scroll)
            self.bind_class("scroll", "<Button-4>", self._on_scroll)  # scroll-up
            self.bind_class("scroll", "<Button-5>", self._on_scroll)  # scroll-down

    def configure_canvas(self, event=None):
        """Configure the canvas as frame is configured."""
        w, h = self._frame.winfo_reqwidth(), self._frame.winfo_reqheight()
        self._canvas.config(scrollregion=(0, 0, w, h), width=w)

    def configure_frame(self, event=None):
        """Configure the frame as the canvas is configured."""
        self._canvas.itemconfigure(self.fid, width=self._canvas.winfo_width())

    if sys.platform == "win32":
        def _on_scroll(self, e: tk.Event):
            """scroll event listener for win32 platform."""
            self._canvas.yview_scroll(-(e.delta // 120), "units")

    elif sys.platform == "linux":
        def _on_scroll(self, e: tk.Event):
            """scroll event listener for linux platform."""
            if e.num == 4:
                self._canvas.yview_scroll(-1, "units")
            elif e.num == 5:
                self._canvas.yview_scroll(1, "units")

    else:
        def _on_scroll(self, e: tk.Event):
            """scroll event listener for unsupported platform."""

    def scroll_to_bottom(self):
        """scrolls to the bottom."""
        self._canvas.yview_moveto(1.0)

    def _setup_theme(self):
        """Setups theme attrs for the child."""
        self._canvas.__theme_attrs__ = self.__theme_attrs__
        self._frame.__theme_attrs__ = self.__theme_attrs__