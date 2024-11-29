import logging
import tkinter as tk
from typing import Callable, Any


logger = logging.getLogger(__name__)


NO_DATA = object()


# TODO - redo this as frozen dataclass
class Binding:
    """A bind object manages a widget's single binding."""

    def __init__(self,
        widget: tk.Widget,
        sequence: str,
        callback: Callable[[tk.Event | None, Any | object], None],
        *,
        data: Any = NO_DATA,
        bind: bool = True, # TODO - remove this
    ):
        """
        Arguements:
        * widget - tkinter widget.
        * sequence - event sequence (can be virtual).
        * callback - callback invoked during event.
        * data - data to be passed with callback.
        * bind - bind on initilisation.
        """
        self.widget = widget
        self.seq = sequence
        self.cb = callback
        self.data = data
        self._id = None

        if bind:
            self.bind()

    # TODO - make this implicit during initilization
    def bind(self):
        """Binds the sequence to the widget."""
        if self._id is None:
            self._id = self.widget.bind(self.seq, self.callback, "+")
            logger.debug(f"Binded {self.seq} to {self.cb.__name__}")
        else:
            logger.debug(f"{self.widget} is already binded on {self.seq}")

    # TODO - remove this
    def unbind(self):
        """Unbind the widget with sequence."""
        if self._id is not None:
            self.widget.unbind(self.seq, self._id)
            self._id = None

    # TODO - remove this
    def rebind(self, sequence: str = "", callback: Callable[[tk.Event | None, Any | object], None] | None = None):
        """Bind the widget again."""
        self.unbind()
        self.seq = sequence or self.seq
        self.cb = callback or self.cb
        self.bind()

    def callback(self, event: tk.Event | None = None):
        """Configured callback."""
        logger.debug(f"Invoking callback for {self.widget} on {self.seq}")

        if not callable(self.cb):
            logger.warning(f"Callback not callable for {self.widget} on {self.seq}")
            return

        try:
            self.cb(event, self.data)
        except tk.TclError:
            logger.exception(f"Failed to call {self.cb.__name__} for {self.widget} on {self.seq}")
