"""Deprecated OSC compatibility package.

The supported MCP runtime uses the local Bitwig Grid Bridge transport. These
classes remain importable for legacy direct callers and are not started by
default.
"""

from .client import BitwigOSCClient
from .controller import BitwigOSCController
from .server import BitwigOSCServer

__all__ = ["BitwigOSCClient", "BitwigOSCController", "BitwigOSCServer"]
