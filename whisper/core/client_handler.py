import asyncio
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, Tuple, Any


@dataclass
class ConnHandle:
    """A client connection."""

    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    data: Dict[str, Any] = field(default_factory=dict)
    run: bool = field(init=False, default=True)

    @cached_property
    def address(self) -> Tuple[str, int]:
        """Provides the address of the client."""
        return self.writer.get_extra_info("peername")

    def get(self, key: str, default: Any = None) -> Any:
        """Provides the data stored about client."""
        return self.data.get(key, default)

    def insert(self, key: str, value: Any):
        """sets the data on user."""
        self.data[key] = value

    @property
    def username(self) -> str | None:
        """Provides the username of the client."""
        return self.get("username", None)

    @property
    def name(self) -> str:
        """Provides the name for connection."""
        return self.username or str(self.address)

    def __str__(self) -> str:
        return f"<ConnHandle: {self.address} as {self.username}>"

    __repr__ = __str__

    async def read(self, n: int) -> bytes:
        """Reads n bytes from stream."""
        return await self.reader.read(n)

    async def write(self, data: bytes):
        """Writes the data into stream."""
        self.writer.write(data)
        await self.writer.drain()
