"""
This module provides server cli parser function.
"""

from argparse import ArgumentParser

from whisper.cli import HostAction, PortAction


def get_parser(program: str, description: str) -> ArgumentParser:
    """Provides parser instance."""

    parser = ArgumentParser(prog=program, description=description)

    parser.add_argument(
        "-ip", "--host",
        metavar="HOST",
        type=str,
        action=HostAction,
        required=False,
        default="localhost",
        help="server host address",
    )

    parser.add_argument(
        "-p", "--port",
        metavar="PORT",
        type=int,
        action=PortAction,
        required=False,
        default=12345,
        help="server port number",
    )

    return parser
