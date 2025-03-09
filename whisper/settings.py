"""
This module provides settings manager for the app.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(kw_only=True)
class AppConfig: # TODO
    """Application configuration."""

    host: str = field(default="127.0.0.1")
    port: int = field(default=50_005)
    username: str = field(default="")

    def as_dict(self) -> Dict[str, Any]:
        """Provide the config as dict object."""
        return self.__getstate__() # type: ignore


@dataclass(frozen=True, repr=False, eq=False, match_args=False)
class Setting: # TODO
    """Settings manager for the application."""

    _config: AppConfig
    _default: AppConfig = field(default_factory=AppConfig, init=False)

    @classmethod
    def from_defaults(cls):
        """Create from default settings."""
        return cls(AppConfig())

    def get(self, key: str) -> Any:
        """Get the setting value."""
        return getattr(self._config, key)

    # TODO - this should be done later

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
