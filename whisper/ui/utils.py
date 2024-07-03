import tkinter as tk


def dynamic_text_height(widget: tk.Text, max_lines: int):
        """Configure the height of widget as the text updates."""
        height = int(widget.index("end - 1c").split(".")[0])
        widget.config(height=min(height, max_lines))
