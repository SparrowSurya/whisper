import asyncio
import unittest

from whisper.packet import PacketRegistery
from .packet_class import TestPacket


class TestPacketInstanceFromStream(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        PacketRegistery.packets[TestPacket.version()] = TestPacket

    @classmethod
    def tearDownClass(cls):
        del PacketRegistery.packets[TestPacket.version()]

    def read_data(self, n: int):
        return b"\x00" * n

    async def reader(self, n: int):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.read_data, n)

    async def test_should_provide_instance(self):
        p = await TestPacket.from_stream(self.reader)
        self.assertIsInstance(p, TestPacket)


class TestPacketInstanceCreation(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        PacketRegistery.packets[TestPacket.version()] = TestPacket

    @classmethod
    def tearDownClass(cls):
        del PacketRegistery.packets[TestPacket.version()]

    async def test_should_provide_instance_from_create(self):
        p = TestPacket.create(b"")
        self.assertIsInstance(p, TestPacket)

    async def test_should_provide_instance_from_request(self):
        p = TestPacket.request(b"")
        self.assertIsInstance(p, TestPacket)

    async def test_should_provide_instance_from_response(self):
        p = TestPacket.response(b"")
        self.assertIsInstance(p, TestPacket)


class TestPacketMethods(unittest.TestCase):

    def setUp(self):
        self.p = TestPacket(b"")

    def tearDown(self):
        self.p = None

    def test_to_stream(self):
        self.assertEqual(self.p.to_stream(), b"\x00")

    def test_content(self):
        self.assertEqual(self.p.contents(), b"")
