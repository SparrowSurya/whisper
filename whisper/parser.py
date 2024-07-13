from enum import Enum
import logging
import re
import argparse


class HostAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        HOSTIP_PATTERN = (
            "^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}"
            "(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"
        )
        values = values.lower()
        if values == "localhost" or re.match(HOSTIP_PATTERN, values):
            setattr(namespace, self.dest, values)
        else:
            parser.error(f"Inavlid hostip. Got: {values}")


class PortAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not isinstance(values, int) or values not in range(0, 2**16):
            parser.error(
                f"Port number must be a positive integer between 0 - {2**16}. Got: {values}"
            )
        setattr(namespace, self.dest, values)


class UserAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) not in range(3, 16):
            parser.error(f"Username should use 3-15 characters. Got: {values}")
        setattr(namespace, self.dest, values)


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL



parser = argparse.ArgumentParser(
    "whisper",
    description="Local self hosted chat platfom",
)

subparsers = parser.add_subparsers(
    dest="command",
    help="sub-command help",
)


server_parser = subparsers.add_parser("server", help="run chat server")

server_parser.add_argument(
    "-ip", "--host",
    metavar="HOST",
    type=str,
    action=HostAction,
    required=True,
    help="ip addres of the server",
)

server_parser.add_argument(
    "-p", "--port",
    metavar="PORT",
    type=int,
    action=PortAction,
    required=True,
    help="port number",
)

server_parser.add_argument(
    "-g", "--log",
    metavar="LOG",
    type=LogLevel,
    choices=tuple(LogLevel),
    required=False,
    default=LogLevel.INFO,
    help="logging level",
)


client_parser = subparsers.add_parser("client", help="run chat client")

client_parser.add_argument(
    "-ip", "--host",
    metavar="HOST",
    type=str,
    action=HostAction,
    required=True,
    help="ip addres of the server",
)

client_parser.add_argument(
    "-p", "--port",
    metavar="PORT",
    type=int,
    action=PortAction,
    required=True,
    help="port number",
)

client_parser.add_argument(
    "-u", "--user",
    metavar="USERNAME",
    type=str,
    action=UserAction,
    required=True,
    help="username in the chat",
)

client_parser.add_argument(
    "-g", "--log",
    metavar="LOG",
    type=LogLevel,
    choices=tuple(LogLevel),
    required=False,
    default=LogLevel.INFO,
    help="logging level",
)