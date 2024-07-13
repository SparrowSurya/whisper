import unittest

from whisper.core.streamcodec import StreamEncoder, StreamDecoder


class TestCodec(unittest.TestCase):

    def test_encode_decode(self):
        data = {"kind": "message", "text": "hi"}
        encoding = "utf-8"

        encoder = StreamEncoder(**data)
        encoded_data = encoder.encode(encoding)

        decoder = StreamDecoder()
        decoded_data = decoder.decode(encoded_data)

        self.assertEqual(data, decoded_data)