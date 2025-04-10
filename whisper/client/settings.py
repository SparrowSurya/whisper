"""
This module provides settings manager class for client application to
manage the application configuration and user data.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(kw_only=True, slots=True, repr=False)
class ClientConfig:
    """Stores the client configuration."""

    host: str = field(default="127.0.0.1")
    port: int = field(default=50_005)

    def as_dict(self) -> Dict[str, Any]:
        """Provide configuration as dict object."""
        return self.__getstate__() # type: ignore


@dataclass(frozen=True, repr=False, eq=False, match_args=False)
class ClientSetting:
    """Cliennt Setting manager."""

    _config: ClientConfig
    """Application configuration."""

    data: Dict[str, Any] = field(default_factory=dict)
    """User data."""

    @classmethod
    def defaults(cls, **kwargs):
        """Use default values."""
        return cls(ClientConfig(**kwargs))

    def get(self, key: str) -> Any:
        """Get the configuration value."""
        return getattr(self._config, key)

    def set(self, key: str, value: Any):
        """Sets the config if the key is present."""
        if hasattr(self._config, key):
            setattr(self._config, key, value)
        else:
            raise KeyError(f"`{key}` does not exist, maybe use `set_data`.")

    def __call__(self, key: str) -> Any:
        return self.get(key)

    # TODO - this will be done later

    # @classmethod
    # def get_default_filepath(cls) -> str:
    #     """Look for `settings.json` in `data` directory of cwd."""
    #     return str(Path("data", "settings.json"))

    # @classmethod
    # def from_dict(cls, cfg: Dict[str, Any]):
    #     return cls(**cfg)

    # @classmethod
    # def from_json_file(cls, fp: str):
    #     fp = fp or cls.get_default_filepath()
    #     with open(fp, "r") as f:
    #         cfg = json.load(f)
    #     return cls.from_dict(cfg)

    # def save(self, fp: str = ""):
    #     """Save the current settings."""
    #     fp = fp or self.get_default_filepath()
    #     with open(fp, "w") as f:
    #         cfg = self._config.as_dict()
    #         content = json.dumps(cfg)
    #         f.truncate(0)
    #         f.write(content)
