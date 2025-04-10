"""
This module provides cli objects used by client and server cli.
"""

import re
import argparse


class HostAction(argparse.Action):
    HOSTIP_PATTERN = (
        "^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}"
        "(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"
    )

    def __call__(self, parser, namespace, values, option_string=None):
        values = values.lower()
        if values == "localhost" or re.match(self.HOSTIP_PATTERN, values):
            return setattr(namespace, self.dest, values)
        parser.error(f"Inavlid hostip. Got: {values}")


class PortAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not isinstance(values, int) or values not in range(0, 2**16):
            parser.error(
                f"Port number must be a positive integer between 0 - {2**16}."
                f" Got: {values}")
        setattr(namespace, self.dest, values)
