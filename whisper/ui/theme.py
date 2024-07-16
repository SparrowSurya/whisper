from dataclasses import dataclass, field
from typing import Mapping


@dataclass(repr=False)
class Theme:
    """
    Theme definition for ui. Supports semantic color system.
    
    """

    name: str
    """Name of the theme."""

    primary: str
    secondary: str
    tertiary: str

    accent: str

    heading: str
    title: str
    text: str

    def __str__(self) -> str:
        self.name

    __repr__ = __str__



class ThemeMixin:
    """Theme mixin class for ui widgets.
    This allows to change the colored attributes of the widget.

    Methods:
    * `get_theme_attrs` - define the attributes which can be styled.
    * `apply_theme` - control the theme applied on itself and children.
    * `apply_theme_self` - control the theme applied on widget itself.
    * `apply_theme_child` = control the theme applied on child widget.
    """

    __theme_attrs__: Theme | None = None
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
