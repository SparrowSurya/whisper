"""
This module contains form validators functions.
"""

from typing import Any, Tuple


def _result(res: bool, on_true: str, on_false: str) -> Tuple[bool, str]:
    return res, (on_true if res else on_false)


def required(value: Any) -> Tuple[bool, str]:
    """Check if value is not empty."""
    MESSAGE = "This field is required"
    if value is None:
        return False, MESSAGE
    if hasattr(value, "__len__"):
        if isinstance(value, str):
            return _result(value.strip() != "", value, MESSAGE)
        return _result(len(value) != 0, value, MESSAGE)
    if isinstance(value, dict):
        return _result(len(value.keys()) != 0, value, MESSAGE)
    return _result(bool(value), value, MESSAGE)
