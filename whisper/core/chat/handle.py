from dataclasses import dataclass
from typing import Callable, Dict, Any


@dataclass(frozen=True)
class Handle:
    """Handle to manage the incoming/outgoing messages in the chat."""

    send: Callable[[Dict[str, Any]], None]
    """This send the content to the server."""

    recv: Callable[[Dict[str, Any]], None]
    """This receives the contentfrom server."""
