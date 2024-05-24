from __future__ import annotations
import asyncio
import threading
from typing import Sequence

from .core.app import BaseApp
from .window import Window


class App(Window, BaseApp):
    """
    Main Application connecting frontend with backend.
    Additionally, command line arguments can be provided using `argv`.

    The refrence to the app can be accessed through `app` attribute.
    It should be propagated to each component.

    For example:
    >>> class SomeComponent(...):
    >>>     def __init__(self, master, *args, **kwargs):
    >>>         super().__init__(*args, **kwargs)
    >>>         self.app = master.app
    """

    def __init__(self, argv: Sequence[str], *args, **kwargs):
        """
        * argv: command line arguments excluding the very first argument.
        """
        Window.__init__(self, *args, **kwargs)
        BaseApp.__init__(self, argv)
        self.setup()
        self.__exiting = False

    def start(self):
        """Start the application."""
        thread = threading.Thread(target=self.run)
        try:
            thread.start()
            self.mainloop()
        except BaseException:
            self.close()
            self.mainloop()
        finally:
            thread.join()

    async def read_handle(self):
        """Coroutine that reads data from server."""
        try:
            while not self.__exiting:
                data = await self.conn.read(4096)
                if data:
                    self.manager.dispatch(data)
        except asyncio.CancelledError:
            pass
        except RuntimeError:
            pass

    def init_tasks(self):
        """Tasks that are required to run early in event loop."""
        self.create_task(self.read_handle())
        set_name = {
            "type": "set-name",
            "name": self.args.user,
        }
        self.create_task(self.conn.write(self.manager.serialize(set_name)))

    def close(self):
        """Closes the application."""
        if not self.__exiting:
            exit_msg = {"type": "exit"}
            self.create_task(
                self.conn.write(self.manager.serialize(exit_msg)),
                on_done=lambda fut: self.stop(),
            )
            self.__exiting = True

    @property
    def app(self) -> App:
        """A refrence to itself."""
        return self

    def setup(self):
        """Application setup."""
        self.setup_root()
        self.apply_config()
        self.on_close(self.close)
        self.exit_fut.add_done_callback(
            lambda fut: self.event_generate(self.DESTORY_EVENT)
        )

    def apply_config(self):
        """Configure app settings."""
        self.set_title("Whisper")
        self.set_geometry(400, 500, 30, 30)
        self.root.chat.topbar.set_title(self.args.user)
