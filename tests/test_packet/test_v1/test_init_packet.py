import unittest

from whisper.test_utils import stream_reader
from whisper.packet import Packet
from whisper.packet.v1 import PacketType, Status, InitV1Packet


class TestInitPacketV1Instantiation(unittest.TestCase):

    def test_create_request_packet_success(self):
        p = InitV1Packet.request(username="TestUser")
        self.assertIsInstance(p, InitV1Packet)

    def test_create_response_packet_success(self):
        p = InitV1Packet.response(status=Status.SUCCESS, username="TestUser", key="123")
        self.assertIsInstance(p, InitV1Packet)


class TestInitPacketV1InstanceFromStream(unittest.IsolatedAsyncioTestCase):

    async def test_should_provide_instance(self):
        reader = stream_reader(b"\x01\x01\x15\x00\x00{'username': 'Happy'}")
        p = await Packet.from_stream(reader)
        self.assertIsInstance(p, InitV1Packet)


class TestInitPacketV1Methods(unittest.TestCase):

    def setUp(self):
        self.username = "TestUser"
        self.p = InitV1Packet.request(username=self.username)

    def tearDown(self):
        self.p = None

    def test_to_stream(self):
        data = self.p.to_stream()
        self.assertIsInstance(data, bytes)

    def test_contents(self):
        contents = self.p.contents()
        self.assertDictEqual(contents, {"username": self.username})

    def test_packet_type(self):
        self.assertEqual(self.p.packet_type(), PacketType.INIT)
