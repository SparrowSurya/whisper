from ui.titlebar import Titlebar as _Titlebar


class Titlebar(_Titlebar):

    def __init__(self, master, *args, height: int, **kwargs):
        super().__init__(master, *args, height=height, **kwargs)
        self.config_theme()

    def config_theme(self):
        """Configure the theme for titlebar."""
        self.icon.__theme_attrs__ = {
            "background": "surfaceContainerLowest",
        }

        self.title.__theme_attrs__ = {
            "background": "surfaceContainerLowest",
            "foreground": "onSurface",
        }

        self.minimize.__theme_attrs__ = {
            "background": "surfaceContainerLowest",
            "foreground": "onSurface",
            "activebackground": "surfaceBright",
            "activeforeground": "onSurface",
        }

        self.maximize.__theme_attrs__ = {
            "background": "surfaceContainerLowest",
            "foreground": "onSurface",
            "activebackground": "surfaceBright",
            "activeforeground": "onSurface",
        }

        self.close.__theme_attrs__ = {
            "background": "surfaceContainerLowest",
            "foreground": "onSurface",
            "activebackground": "onError",
            "activeforeground": "onSurface",
        }

        self.minimize.bind(
            "<Enter>",
            lambda _: self.minimize.config(background=self.master.theme.surfaceContainerHigh),
        )
        self.minimize.bind(
            "<Leave>",
            lambda _: self.minimize.config(background=self.master.theme.surfaceContainerLowest),
        )

        self.maximize.bind(
            "<Enter>",
            lambda _: self.maximize.config(background=self.master.theme.surfaceContainerHigh),
        )
        self.maximize.bind(
            "<Leave>",
            lambda _: self.maximize.config(background=self.master.theme.surfaceContainerLowest),
        )

        self.close.bind(
            "<Enter>",
            lambda _: self.close.config(background=self.master.theme.errorContainer),
        )
        self.close.bind(
            "<Leave>",
            lambda _: self.close.config(background=self.master.theme.surfaceContainerLowest),
        )
