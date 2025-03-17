"""
This module provides a handler class to manage client connections and
their data.
"""

import socket
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(frozen=True, repr=False, order=True, slots=True)
class Address:
    """Tuple of host and port."""

    host: str
    port: int

    def __repr__(self) -> str:
        return f"<Address: ({self.host}, {self.port})>"

    def __str__(self) -> str:
        return f"{self.host}:{self.port}"


@dataclass(repr=False, slots=True)
class ConnHandle:
    """Client connection handler object."""

    sock: socket.socket
    """Underlying socket object."""

    address: Address
    """Address of the connection."""

    data: Dict[str, Any] = field(default_factory=dict)
    """Connection related data."""

    serve: bool = field(default=False, init=False)
    """if the connections is allowed to serve."""

    close: bool = field(default=False, init=False)
    """If connection should be closed."""

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
