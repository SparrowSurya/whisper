"""
This module provides the basic chat room interface.
"""

import abc

class BaseChat(abc.ABC):
    """Basic interface to the chat room."""

    # TODO - manybe instead giving app instance use handler
    def __init__(self, rid: str, app):
        """It requires a chat room id and the app instance for communication."""
        self.rid = rid
        self.app = app

    @abc.abstractmethod
    def show_message(self, **kwargs):
        """Shows the message on the chat."""

    # TODO - pass it to handler
    def send_message(self, **kwargs):
        """Send the message."""
        self.app.send_message(kwargs)
