import unittest

from whisper.packet.v1.base import PacketV1


class TestPacketV1(unittest.TestCase):

    def test_correct_version(self):
        self.assertEqual(PacketV1.version(), 1)

    def test_correct_max_data_size(self):
        self.assertEqual(PacketV1.data_size_limit(), 65530)
