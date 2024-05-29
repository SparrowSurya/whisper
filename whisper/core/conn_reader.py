import asyncio
import json
from typing import Any, Dict, Callable, Awaitable

from .async_conn import AsyncConn


class ConnReader(AsyncConn):
    """Reads the imcoming data on the stream."""

    def __init__(self):
        super().__init__()
        self._buffer = bytes()
        self._header_len: int | None = None
        self._header: Dict[str, Any] | None = None
        self._payload: Dict[str, Any] | None = None

    async def read_conn(self, read: Callable[[], Awaitable[bytes]]):
        """Reads the chunk of data."""
        try:
            while not self.is_open:
                if data := await read():
                    self.process(data)
        except (asyncio.CancelledError, RuntimeError):
            pass

    def process(self, data: bytes):
        """Process the data in buffer."""
        self._buffer += data
        self._process_proto()
        self._process_header()
        self._process_payload()
        if self._payload is not None:
            self.dispatch(self._payload)
            self._header_len = self._header = self._payload = None

    def _process_proto(self):
        if self._header_len is None:
            hdrlen = 2
            if len(self._buffer) >= hdrlen:
                self._header_len = int(self._buffer[:hdrlen].hex(), base=16)
                self._buffer = self._buffer[hdrlen:]

    def _process_header(self):
        if self._header_len is not None and self._header is None:
            if len(self._buffer) >= self._header_len:
                self._header = self.decode(self._buffer[: self._header_len])
                self._buffer = self._buffer[self._header_len :]

    def _process_payload(self):
        if self._header is not None and self._response is None:
            length = self._header["content-length"]
            if len(self._buffer) >= length:
                self._response = self.decode(
                    self._buffer[:length],
                    enc=self._header["encoding"],
                )
            self._buffer = self._buffer[length:]

    def respond(self, content: Dict[str, Any]):
        """Received content fron the conn."""
        print(content)

    def decode(self, data: bytes, enc: str = "utf-8") -> Dict[str, Any]:
        """JSON decoder."""
        return json.loads(data.decode(enc))
