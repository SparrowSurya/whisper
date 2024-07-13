import socket
from dataclasses import dataclass, field
from typing import Dict, Tuple, Any


@dataclass(repr=False, slots=True)
class ConnectionHandle:
    """
    The class is a frozen dataclass which wraps the underlying objects
    and data. The `data` is an dictionary attribute containing the
    information related to connection.
    """

    sock: socket.socket
    """Underlying socket object."""

    address: Tuple[str, int]
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

    @property
    def name(self) -> str:
        """Provides the name for connection."""
        return self.username or str(self.address)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        if self.username:
            return f"<{type(self).__name__}: {self.address} as {self.username}>"
        return f"<{type(self).__name__}: {self.address}>"
