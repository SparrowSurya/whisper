from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Sequence

from .window import Window


@dataclass(frozen=True)
class Args:
    """Command line arguments."""

    user: str


class App(Window):
    """
    Manages window and events.
    """

    def __init__(self, argv: Sequence[str], *args, **kwargs):
        self.argv = self.parse_args(argv)
        super().__init__(*args, **kwargs)
        self.setup()

    def setup(self):
        """Setup everything in the application."""
        self.set_title("Whisper")
        self.set_geometry(400, 500, 30, 30)
        self.setup_root()
        print(self.argv.user)
        self.root.chatbox.set_username(self.argv.user)
        self.late_setup()

    def get_parser(self) -> ArgumentParser:
        """Provides the parser object to parse the arguments to the application."""
        parser = ArgumentParser()

        parser.add_argument(
            "-u", "--user", type=str, required=True, help="username displayed on chat."
        )

        return parser

    def parse_args(self, argv: Sequence[str]) -> Args:
        """Provides a data object with parsed arguments."""
        parser = self.get_parser()
        args = parser.parse_args(argv)
        return Args(
            user=args.user,
        )

    def run(self):
        """Application mainloop."""
        self.mainloop()
