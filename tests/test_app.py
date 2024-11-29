import time
import socket
import asyncio
import unittest
import threading

from whisper.app import Application as App


class TestApp(unittest.TestCase):

    def test_app_open_close_success(self):
        app = App()
        app.after(800, app.shutdown)
        app.mainloop()

    # FIXME: there is a better way to test the backend working as
    # expected. currently works with an error raised in worker coroutine
    def test_app_backend_runs_success(self):
        def server(app):
            client = None
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("127.0.0.1", 50_005))
            server.settimeout(2)
            server.listen(1)
            try:
                client, addr = server.accept()
                app.shutdown()
                time.sleep(1)
            except socket.timeout:
                pass
            finally:
                if client:
                    client.close()
                server.close()

        app = App()
        app.after(500, app.run_thread)
        app.after(1000, app.shutdown)

        thread = threading.Thread(target=server, args=(app,), name="DummyServer")
        thread.start()

        app.mainloop()
        thread.join()
