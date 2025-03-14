"""
This module provide packet handlersfor each packet kind.
"""

import abc


class ClientHandler(abc.ABC):
    """Handles specific packet kind."""

    def __init__(self, client):
        self.client = client

    @abc.abstractmethod
    def __call__(self, **kwargs):
        """Handles the packet content."""
