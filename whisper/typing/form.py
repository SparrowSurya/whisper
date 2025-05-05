"""
This module provides type annotations for form widgets.
"""

from typing import Tuple, Dict, Any, Callable, Mapping, Literal, Unpack


FormActionType = Literal["submit", "cancel", "reset"]
Validator = Callable[[Any], Tuple[bool, Any]]

FormSubmitCmd = Callable[[Unpack[Dict[str, Any]]], None]
FormCancelCmd = Callable[[], None]
FormResetCmd = Callable[[], Mapping[str, Any] | None]
