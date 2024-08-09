from dataclasses import dataclass
import json
from typing import Mapping, Self, Dict


@dataclass(repr=False, frozen=True)
class Theme:
    """
    Theme definition for ui. Supports semantic color system.
    """

    name: str
    """Name of the theme."""

    primary: str
    surfaceTint: str
    onPrimary: str
    primaryContainer: str
    onPrimaryContainer: str

    secondary: str
    onSecondary: str
    secondaryContainer: str
    onSecondaryContainer: str

    tertiary: str
    onTertiary: str
    tertiaryContainer: str
    onTertiaryContainer: str

    error: str
    onError: str
    errorContainer: str
    onErrorContainer: str

    background: str
    onBackground: str

    surface: str
    onSurface: str
    surfaceVariant: str
    onSurfaceVariant: str

    outline: str
    outlineVariant: str

    shadow: str
    scrim: str

    inverseSurface: str
    inverseOnSurface: str
    inversePrimary: str

    primaryFixed: str
    onPrimaryFixed: str
    primaryFixedDim: str
    onPrimaryFixedVariant: str
    secondaryFixed: str
    onSecondaryFixed: str
    secondaryFixedDim: str
    onSecondaryFixedVariant: str

    tertiaryFixed: str
    onTertiaryFixed: str
    tertiaryFixedDim: str
    onTertiaryFixedVariant: str

    surfaceDim: str
    surfaceBright: str
    surfaceContainerLowest: str
    surfaceContainerLow: str
    surfaceContainer: str
    surfaceContainerHigh: str
    surfaceContainerHighest: str

    variant: str = ""
    """Theme variant name."""

    def __str__(self) -> str:
        self.name

    __repr__ = __str__

    @classmethod
    def from_json(cls, filepath: str) -> Self:
        """"Load theme from json file."""
        with open(filepath, "r") as f:
            content = json.load(f)
        return cls(**content)


class ThemeMixin:
    """Theme mixin class for ui widgets.
    This allows to change the colored attributes of the widget.

    Methods:
    * `get_theme_attrs` - define the attributes which can be styled.
    * `apply_theme` - control the theme applied on itself and children.
    * `apply_theme_self` - control the theme applied on widget itself.
    * `apply_theme_child` = control the theme applied on child widget.
    """

    __theme_attrs__: Dict[str, str] | None = None
    """Defines the semantic name for each attribute."""

    def get_theme_attrs(self) -> Mapping[str, str]:
        """Key value mapping object which maps the property of widget that can
        be styled."""
        return self.__theme_attrs__ or {}

    def apply_theme(self, theme: Theme):
        """Apply the theme to the widget and its children."""
        self.apply_theme_self(theme)
        self.apply_theme_child(theme)

    def apply_theme_self(self, theme: Theme):
        """Apply theme to itself."""
        attrs = self.get_theme_attrs()
        config = {attr: getattr(theme, scheme) for attr, scheme in attrs.items()}
        if config:
            self.configure(**config)

    def apply_theme_child(self, theme: Theme):
        """Apply theme to the children."""
        for child in self.winfo_children():
            child.apply_theme(theme)
