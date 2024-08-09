from ui.widgets import Text


class MultilineTextInput(Text):
    """A custom text input widget for multiline text input."""

    lines = 5
    """Number of lines at max that will be displayed."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.bind("<KeyRelease>", self.configure_lines, "+")

    # TODO - as per tkinter the lines are counted as count of newline
    # characters. Hence, the lines that exceeds the width of the widget
    # will not be shown.
    def configure_lines(self, event=None):
        """COnfigure the lines displayed."""
        height = int(self.index("end - 1c").split(".")[0])
        self.config(height=min(height, self.lines))
