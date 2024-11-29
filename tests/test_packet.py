import asyncio
import unittest

from whisper.core.packet import Packet, PacketV1, PacketKind, PacketRegistery


async def fake_await():
    """Simulate fake await."""
    await asyncio.sleep(0.0)


class FakeConnection:
    """Fake connection object."""

    def __init__(self):
        self.buffer = b""

    async def read(self, n: int) -> bytes:
        await fake_await()
        data, self.buffer = self.buffer[:n], self.buffer[n:]
        return data

    async def write(self, d: bytes) -> None:
        await fake_await()
        self.buffer += d


class TestBasePacket(unittest.IsolatedAsyncioTestCase):

    @PacketRegistery.register
    class PacketV0(Packet):

        @classmethod
        def get_version(self):
            return 0

        @classmethod
        async def from_stream(cls, reader):
            await fake_await()
            return cls()

        def to_stream(self):
            return super().to_stream()

    def get_packet_cls(self):
        return self.PacketV0

    def setUp(self):
        self.conn = FakeConnection()

    async def test_read_write_success(self):
        packet_cls = self.get_packet_cls()
        packet_sent = packet_cls()
        data = packet_sent.to_stream()

        await self.conn.write(data)
        packet_recv = await Packet.from_stream(self.conn.read)

        self.assertEqual(self.conn.buffer, b"")
        self.assertIsInstance(packet_recv, packet_cls)


class TestPacketV1(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.conn = FakeConnection()
        self.packet = PacketV1(
            PacketKind.EXIT,
            b"Hello, World!"
        )

    async def test_read_write_success(self):
        data = self.packet.to_stream()
        await self.conn.write(data)

        reader = self.conn.read
        packet = await Packet.from_stream(reader)

        self.assertEqual(self.conn.buffer, b"")
        self.assertEqual(packet, self.packet)
