import tkinter as tk
from typing import Callable, Any


class Binding:
    """A bind object manages a widget's single binding."""

    def __init__(self,
        widget: tk.Widget,
        sequence: str,
        callback: Callable[[tk.Event, Any], None] | Callable[[], None],
        *,
        data: Any | None = None,
        bind: bool = False,
    ):
        """
        Arguements:
        * widget - tkinter widget.
        * sequence - event sequence (can be virtual).
        * callback - callback invoked.
        * data - data to be passed with callback
        * bind - bind on initilisation.
        """
        self.widget = widget
        self.sequence = sequence
        self._callback = callback
        self._data = data
        self._id = None

        if bind:
            self.bind()

    def bind(self):
        """Binds the sequence to the widget."""
        if self._id is not None:
            self._id = self.widget.bind(self.sequence, self.callback, "+")

    def unbind(self):
        """Unbind the widget with sequence."""
        if self._id is not None:
            self.widget.unbind(self.sequence, self._id)
            self._id = None

    def rebind(self):
        """Bind the widget again."""
        self.unbind()
        self.bind()

    def __del__(self):
        self.unbind()

    def callback(self, event: tk.Event | None = None):
        """Configured callback."""
        if event and self._data:
            return self._callback(event=event, data=self.data)
        if event:
            return self._callback(event=event)
        if self.data:
            return self._callback(data=self.data)
        return self._callback()