import unittest

from whisper.test_utils import stream_reader
from whisper.packet import Packet
from whisper.packet.v1 import PacketType, Status, ExitReason, ExitV1Packet


class TestExitPacketV1Instantiation(unittest.TestCase):

    def test_create_request_packet_success(self):
        p = ExitV1Packet.request(reason=ExitReason.SELF_EXIT)
        self.assertIsInstance(p, ExitV1Packet)

    def test_create_response_packet_success(self):
        p = ExitV1Packet.response(reason=ExitReason.SELF_EXIT, status=Status.SUCCESS)
        self.assertIsInstance(p, ExitV1Packet)


class TestExitPacketV1InstanceFromStream(unittest.IsolatedAsyncioTestCase):

    async def test_should_provide_instance(self):
        reader = stream_reader(b"\x01\x00\x01\x00\x00\x10")
        p = await Packet.from_stream(reader)
        self.assertIsInstance(p, ExitV1Packet)


class TestExitPacketV1Methods(unittest.TestCase):

    def setUp(self):
        self.reason = ExitReason.SELF_EXIT
        self.p = ExitV1Packet.request(reason=self.reason)

    def tearDown(self):
        self.p = None

    def test_to_stream(self):
        data = self.p.to_stream()
        self.assertIsInstance(data, bytes)

    def test_contents(self):
        contents = self.p.contents()
        self.assertEqual(contents, self.reason)

    def test_packet_type(self):
        self.assertEqual(self.p.packet_type(), PacketType.EXIT)
