import sys
import tkinter as tk

from .container import Container


class ScrollableContainer(Container):
    """Base scrollable container.

    Use `frame` object as master to child widgets.
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._setup_scroll(*args, **kwargs)

    def _setup_scroll(self, *args, **kwargs):
        """Setup scroll on the container."""
        self._canvas = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self._canvas.pack(fill="both", expand=1)

        self.frame = Container(self._canvas, *args, **kwargs)
        self.fid = self._canvas.create_window(0, 0, anchor="nw", window=self.frame)

        self.frame.bind("<Configure>", self.configure_canvas)
        self._canvas.bind("<Configure>", self.configure_frame)

        if sys.platform == "win32":
            self._on_scroll = self._on_scroll_win32
            self._canvas.bind("<MouseWheel>", self._on_scroll)
            self.bind_class("scroll", "<MouseWheel>", self._on_scroll)
        elif sys.platform == "linux":
            self._on_scroll = self._on_scroll_linux
            self._canvas.bind("<Button-4>", self._on_scroll)
            self._canvas.bind("<Button-5>", self._on_scroll)
            self.bind_class("scroll", "<Button-4>", self._on_scroll)  # scroll-up
            self.bind_class("scroll", "<Button-5>", self._on_scroll)  # scroll-down
        else:
            self._on_scroll = self._on_scroll_empty

    def configure_canvas(self, event=None):
        """Configure the canvas as frame is configured."""
        w, h = self.frame.winfo_reqwidth(), self.frame.winfo_reqheight()
        self._canvas.config(scrollregion=(0, 0, w, h), width=w)

    def configure_frame(self, event=None):
        """Configure the frame as the canvas is configured."""
        self._canvas.itemconfigure(self.fid, width=self._canvas.winfo_width())

    def _on_scroll_win32(self, e: tk.Event):
        """scroll event listener for win32 platform."""
        self._canvas.yview_scroll(-(e.delta // 120), "units")

    def _on_scroll_linux(self, e: tk.Event):
        """scroll event listener for linux platform."""
        if e.num == 4:
            self._canvas.yview_scroll(-1, "units")
        elif e.num == 5:
            self._canvas.yview_scroll(1, "units")

    def _on_scroll_empty(self, e: tk.Event):
        """scroll event listener for unsupported platform."""
        print("Scrolling is not supported on your platform.")

    def scroll_to_bottom(self):
        """scrolls to the bottom."""
        self._canvas.yview_moveto(1.0)
