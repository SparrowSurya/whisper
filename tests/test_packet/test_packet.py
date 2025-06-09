import unittest

from whisper.test_utils import stream_reader
from whisper.packet import PacketRegistery
from .packet_class import TestPacket


class TestPacketInstanceFromStream(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        PacketRegistery.packets[TestPacket.version()] = TestPacket

    @classmethod
    def tearDownClass(cls):
        del PacketRegistery.packets[TestPacket.version()]

    async def test_should_provide_instance(self):
        p = await TestPacket.from_stream(stream_reader(b"\x00\x00"))
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
