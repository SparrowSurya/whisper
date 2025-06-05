from whisper.packet import Packet


class TestPacket(Packet):
    """Simple test packet with no additional data."""

    @staticmethod
    def version():
        return 0

    @classmethod
    async def from_stream(cls, reader):
        return cls(await reader(1))

    @classmethod
    def create(cls, msg: str | bytes):
        return cls(msg)

    @classmethod
    def request(cls, msg: str | bytes):
        return cls.create(msg)

    @classmethod
    def response(cls, msg: str | bytes):
        return cls.create(msg)

    @classmethod
    def unique_key(cls):
        return cls.version()

    def contents(self):
        return self.data

    def to_stream(self):
        return super().to_stream() + self.data
