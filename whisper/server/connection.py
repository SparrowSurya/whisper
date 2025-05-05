"""
This module provides a handler class to manage client connections and their data.
"""

import socket
from typing import Dict, Any

from whisper.common import Address


class ConnHandle:
    """Client connection handler object."""

    __slots__ = ("sock", "address", "data", "serve", "close")

    def __init__(self, sock: socket.socket, addr: Address, data: Dict[str, Any]):
        self.sock = sock
        self.address = addr
        self.data = data
        self.serve = False
        self.close = False

    @property
    def username(self) -> str | None:
        """Provides the username of the client."""
        return self.data.get("username", None)

    @username.setter
    def username(self, username: str):
        """Sets username of the client."""
        self.data["username"] = username

    @property
    def name(self) -> str:
        """Provides the name for connection."""
        return self.username or str(self.address)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self.address}>"

    def __hash__(self) -> int:
        return self.sock.__hash__()
