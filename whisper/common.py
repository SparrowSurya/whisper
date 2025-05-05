"""
This file provides shared objects.
"""


class Address(tuple):
    """Tuple based address object."""

    def __new__(cls, host: str, port: int):
        return super().__new__(cls, (host, port))

    @property
    def host(self) -> str:
        return self[0]

    @property
    def port(self) -> int:
        return self[1]

    def __repr__(self) -> str:
        return f"<Address '{self.host}:{self.port}'>"
