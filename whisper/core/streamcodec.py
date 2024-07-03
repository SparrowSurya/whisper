import json
from collections import namedtuple
from typing import Dict, Any


class Message:
    """It provides various methods to create a message object."""

    @staticmethod
    def create(kind: str, **kwargs) -> object:
        """Arbitrary message.

        Arguments:
        * kind - message or action-name.
        * kwargs - related content.
        """
        keys = list(kwargs.keys()) + ["kind"]
        Object = namedtuple("Object", keys)
        return Object(kind=kind, **kwargs)

    @staticmethod
    def message(text: str, **kwargs):
        """Create a chat message."""
        return Message.create(kind="message", text=text, **kwargs)

    @staticmethod
    def action(name: str, **kwargs):
        """Create an action message."""
        return Message.create(kind=name, **kwargs)


class StreamEncoder:
    """
    Responsible for the format and serialization of the data.
    The content is a dict object converted to JSON.

    Format of the packet:
    +--------+----------------+------------------------+
    |  Hlen  |     Header     |        Payload         |
    +--------+----------------+------------------------+

    1. Hlen: 2-byte data representing the header length.
    2. Header: contains metadata and payload information.
    3. Payload: the content sent out.
    """

    def __init__(self, obj: object, **kwargs):
        """
        Arguments:
        * obj: message being encoded.
        * kwargs: additional arguments.
        """
        self.headers: Dict[str, Any] = {}
        self.obj = obj
        self.kwargs = kwargs

    def add_header(self, name: str, desc: Any):
        """Add or update the existing header."""
        self.headers[name] = desc

    def add_content(self, name: str, value: Any):
        """Add or update the existing data."""
        self.kwargs[name] = value

    def json_encode(self, obj: object, encoding: str) -> bytes:
        """JSON encoide the object."""
        return json.dumps(
            obj,
            ensure_ascii=(encoding.lower() == "ascii"),
        ).encode(encoding)

    def encode(self, encoding: str) -> bytes:
        """Serialize the request into bytes."""
        request = self.obj._asdict()  # type: ignore
        payload = self.json_encode(request, encoding)

        for name, desc in (
            ("encoding", encoding),
            ("content-type", "text/json"),
            ("content-length", len(payload)),
        ):
            self.add_header(name, desc)

        header = self.json_encode(self.headers, "utf-8")
        return len(header).to_bytes(2) + header + payload


class StreamDecoder:
    """
    Responsible for accumulating chunks of data and returning
    the content once enough data been collected.
    """

    def __init__(self):
        self._buffer = bytes()
        self._hlen = None
        self._header = None
        self._payload = None

    def decode(self, data: bytes) -> object | None:
        """
        Process the chunk of data. Returns the content if
        enough data has been collected.
        """
        self._buffer += data
        self._process_proto()
        self._process_header()
        self._process_payload()

        obj = None
        if self._payload is not None:
            obj = Message.create(**self._payload)
            self._hlen = self._header = self._payload = None
        return obj

    def _process_proto(self):
        """This processes the initial information."""
        if self._hlen is None:
            hdrlen = 2
            if len(self._buffer) >= hdrlen:
                self._hlen = int(self._buffer[:hdrlen].hex(), base=16)
                self._buffer = self._buffer[hdrlen:]

    def _process_header(self):
        """This processes the header part."""
        if self._hlen is not None and self._header is None:
            if len(self._buffer) >= self._hlen:
                self._header = self.json_decode(self._buffer[: self._hlen])
                self._buffer = self._buffer[self._hlen :]

    def _process_payload(self):
        """This processes the payload part."""
        if self._header is not None and self._payload is None:
            length = self._header["content-length"]
            if len(self._buffer) >= length:
                self._payload = self.json_decode(
                    self._buffer[:length],
                    self._header["encoding"],
                )
            self._buffer = self._buffer[length:]

    def json_decode(self, data: bytes, encoding: str = "utf-8") -> Dict[str, Any]:
        """Provides the python dict object."""
        return json.loads(data.decode(encoding))
