import asyncio
import unittest

from whisper.core import ServerConn, ClientConn


# helper to create unique port numbers
def port_gen(n):
    yield n
    yield from port_gen(n+1)


HOST = "127.0.0.1"
PORT = port_gen(10_000)


class TestTCPServer(unittest.TestCase):
    host = HOST
    port = next(PORT)

    def test_server_start_and_close(self):
        server = ServerConn()

        # initial state check
        self.assertFalse(server.is_serving)
        with self.assertRaises(RuntimeError):
            server.stop()

        server.start(self.host, self.port)

        # state check after server starts
        self.assertEqual(server.address(), (self.host, self.port))
        self.assertTrue(server.is_serving)
        with self.assertRaises(RuntimeError):
            server.start(self.host, self.port)

        server.stop()

        # state check after server closes
        with self.assertRaises(RuntimeError):
            server.stop()
        self.assertFalse(server.is_serving)


class TestClientConnection(unittest.TestCase):
    host = HOST
    port = next(PORT)

    def setUp(self):
        self.server = ServerConn()
        self.server.start(self.host, self.port)

    def tearDown(self):
        self.server.stop()

    def test_client_connect_and_disconnect(self):
        client = ClientConn()

        # initial state check
        self.assertFalse(client.is_connected)
        with self.assertRaises(RuntimeError):
            client.disconnect()

        client.connect(self.host, self.port)

        # state check after client is connected
        self.assertTrue(client.is_connected)
        with self.assertRaises(RuntimeError):
            client.connect(self.host, self.port)

        client.disconnect()

        # state check after client disconnects
        self.assertFalse(client.is_connected)
        with self.assertRaises(RuntimeError):
            client.disconnect()


class TestReadWrite(unittest.IsolatedAsyncioTestCase):
    host = HOST
    port = next(PORT)

    async def test_read_write(self):
        server = ServerConn()
        client = ClientConn()
        loop = asyncio.get_running_loop()
        data = b"Hello, World!"

        # open connection
        server.start(self.host, self.port)
        client.connect(self.host, self.port)
        conn, _ = await server.accept(loop)

        # client to server
        await client.write(data, loop)
        data_recv = await server.read(conn, len(data), loop)

        self.assertEqual(data, data_recv)

        # server to client
        await server.write(conn, data, loop)
        data_recv = await client.read(1024, loop)

        self.assertEqual(data, data_recv)

        # close connection
        conn.close()
        client.disconnect()
        server.stop()
