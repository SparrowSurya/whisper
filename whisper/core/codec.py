"""
This module provides necessary encoding/decoding functions.
"""

import json
from typing import Dict, Any


def json_encode(data: Dict[str, Any]) -> bytes:
    """Serialize the dict object into stream of bytes."""
    return json.dumps(data).encode(encoding="UTF-8")

def json_decode(data: bytes) -> Dict[str, Any]:
    """Deserialize the stream of bytes into dict object."""
    return json.loads(data.decode(encoding="UTF-8"))
