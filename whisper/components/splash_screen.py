"""
This module provides the splash screen for the client application.
"""

from typing import Dict, Any, Mapping

from whisper.ui import Window, Label, Container
from whisper.components.conn_init_form import ConnInitForm
from whisper.typing import (
    Misc as _Misc,
    FormSubmitCmd as _FormSubmitCmd,
)


class SplashRoot(Container):
    """Root of the splash screen."""

    def __init__(self, master: _Misc, on_submit: _FormSubmitCmd, **kwargs):
        Container.__init__(self, master, **kwargs)
        self.app = master.app

        # TODO: layout
        self.heading = Label(self, text="Initialize")
        self.form = ConnInitForm(self, submit_cb=on_submit)

    def setup(self):
        super().setup()
        self.heading.setup()
        self.form.setup()
        self.heading.pack(fill="x")
        self.form.pack(fill="x")

    def setup(self):
        super().setup()
        self.heading.pack()
        self.form.pack(expand=1)
        self.heading.setup()
        self.form.setup()


class SplashWindow(Window):
    """Splash screen window for client application."""

    def __init__(self, master: _Misc):
        Window.__init__(self, master)
        self.app = master.app
        self.config(padx=1, pady=1)
        self.overrideredirect(True)

        self.root = SplashRoot(self, on_submit=self.on_form_submit, height=320, width=240)
        self.root.bind("<Button-1>", lambda _: self.app.shutdown(None))

    def setup(self):
        super().setup()
        self.root.setup()
        self.root.pack(expand=1, fill="x", padx=40, anchor="center")
        self.center_window(320, 240)
        self.show_window()
        self.app.hide_window()

    def open_window(self,
        values: Dict[str, Any] | None = None,
        errors: Dict[str, Any] | None = None,
    ):
        """Open the window again"""
        self.root.form.setup(values, errors)
        self.show_window()
        self.app.hide_window()

    def open_window(self,
        values: Dict[str, Any] | None = None,
        errors: Dict[str, Any] | None = None,
    ):
        """Open the window again"""
        self.root.form.setup(values, errors)
        self.show_window()

    def on_form_submit(self, **kwargs):
        """Handle conn init form submit."""
        self.app.init_connection(**kwargs)
        self.hide_window()

    def on_form_submit(self, **kwargs):
        """Handle conn init form submit."""
        self.app.init_connection(**kwargs)
        self.hide_window()
