class BaseChat:
    """Base chat class."""

    def __init__(self, app):
        """
        Arguments:
        * app - refers to the main application.
        """
        self.app = app

    def send_message(self, text: str):
        """Message sent in the chat."""
        self.app.send("message", text=text)

    def show_message(self, **kwargs):
        """Message received from server."""
