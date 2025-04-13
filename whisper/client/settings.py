"""
This module provides settings manager class for client application to
manage the application configuration and user data.
"""

from dataclasses import dataclass, field
from typing import Any, Dict

from whisper.ui.theme import Theme


@dataclass(kw_only=True, slots=True, repr=False)
class Config:
    """Client app configuration."""

    host: str = field(default="127.0.0.1")
    port: int = field(default=50_005)

    def as_dict(self) -> Dict[str, Any]:
        """Provide configuration as dict object."""
        return self.__getstate__() # type: ignore


@dataclass(repr=False, eq=False, match_args=False)
class Setting:
    """Cliennt setting manager."""

    cfg: Config
    theme: Theme
    data: Dict[str, Any] = field(default_factory=dict)
