from functools import lru_cache


class Settings:
    """
    Main application settings manager. This controls and  manages the
    settings being applied to the application.

    Usage:
    * config - refers to user settings.
    * defaults - refers to the default setting.
    """

    def __init__(self, app, config):
        """
        The object has two arguments
        Arguements:
        * app - main application.
        * user_config - user settings.
        """
        self.app = app
        self.config = config
        self.defaults = self.load_defaults()

    @lru_cache
    def load_defaults(self):
        """Loads the default app configuration."""

    def apply_defaults(self):
        """Applies default settings on the app."""

    def change_theme(self, theme):
        """Change the application theme."""
