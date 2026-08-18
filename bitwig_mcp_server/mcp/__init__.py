"""
Bitwig MCP integration package.

This package provides MCP (Model Context Protocol) integration for Bitwig Studio.
"""

from .tools import execute_tool, get_bitwig_tools

__all__ = ["get_bitwig_tools", "execute_tool"]
