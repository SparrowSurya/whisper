import json
from typing import Any


class BasePacket:
    """Base packet object with headers only."""

    def __init__(self):
        self.headers = {}

    def add_header(self, name: str, desc: Any):
        self.headers[name] = desc

    def json_serialize(self, obj: object, enc: str = "utf-8") -> bytes:
        return json.dumps(
            obj,
            ensure_ascii=(enc.lower() == "ascii"),
        ).encode(enc)


class Packet(BasePacket):
    """Request packet to manage the data and serialization."""

    def __init__(self, kind: str, enc: str, **kwargs):
        super().__init__()
        self._kind = kind
        self.enc = enc
        self.kwargs = kwargs

    def serialize(self) -> bytes:
        """Serialize the request into bytes."""
        request = {"kind": self._kind, **self.kwargs}
        payload = self.json_serialize(request, self.enc)

        for name, desc in (
            ("encoding", self.enc),
            ("content-type", "text/json"),
            ("content-length", len(payload)),
        ):
            self.add_header(name, desc)

        header = self.json_serialize(self.headers)
        return len(header).to_bytes(2) + header + payload
