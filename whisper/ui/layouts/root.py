"""
This module contains the root widget of the app (after MainWindow).
"""

import tkinter as tk


class Root(tk.Frame):
    """Root widget of the application."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = master.app

        self.start_button = tk.Button(self, text="Start")
        self.start_button.pack(padx=2, pady=4)

        self.exit_button = tk.Button(self, text="Exit")
        self.exit_button.pack(padx=2, pady=4)

        self.start_button.config(command=self.app.run)
        self.exit_button.config(command=self.app.shutdown)
