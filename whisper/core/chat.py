class BaseChat:
    """Basic interface to the chat room."""

    def __init__(self, id: str, app):
        self.id = id
        self.app = app

    def show_message(self, **kwargs):
        """Shows the message on the chat."""
        # TODO - use logging t print messages

    def send_message(self, **kwargs):
        """Send the message."""
        self.app.send_message(kwargs)
