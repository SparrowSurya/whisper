"""
This module contains special utility variables, functions and classes.

### Variable
* NO_DATA - represents absence of data.

### Functions

### Classes
* Binding - tkinter widget event binding.
"""

import tkinter as tk
from typing import Callable, Any



NO_DATA = object()


class Binding:
    """Manages tkinter widget's event binding."""

    def __init__(self,
        widget: tk.Widget,
        sequence: str,
        callback: Callable[[tk.Event | None, Any | object], None],
        *,
        data: Any = NO_DATA,
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
        self.bind()

    def bind(self):
        """Binds the sequence to the widget."""
        if self._id is None:
            self._id = self.widget.bind(self.seq, self.callback, "+")

    def unbind(self):
        """Unbind the widget with sequence."""
        if self._id is not None:
            self.widget.unbind(self.seq, self._id)
            self._id = None

    def call(self, event: tk.Event | None = None):
        """Invokes event callback."""
        try:
            self.cb(event, self.data)
        except tk.TclError:
            pass

    def __del__(self):
        """Cleanup the binding."""
        self.unbind()
