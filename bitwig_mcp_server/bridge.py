"""Client for the standalone Bitwig Grid bridge extension."""

from __future__ import annotations

import json
import socket
from typing import Any


class GridBridgeError(RuntimeError):
    """Raised when the Bitwig-side bridge rejects or cannot handle a request."""


class GridBridgeClient:
    """Small synchronous line-protocol client for the local bridge."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765, timeout: float = 3.0):
        self.host = host
        self.port = port
        self.timeout = timeout

    def request(self, command: str) -> dict[str, Any]:
        try:
            with socket.create_connection((self.host, self.port), self.timeout) as connection:
                connection.sendall((command + "\n").encode("utf-8"))
                response = connection.makefile("r", encoding="utf-8").readline()
        except OSError as error:
            raise GridBridgeError(f"Bridge unavailable at {self.host}:{self.port}: {error}") from error
        try:
            payload = json.loads(response)
        except json.JSONDecodeError as error:
            raise GridBridgeError(f"Invalid bridge response: {response!r}") from error
        if not payload.get("ok", False):
            raise GridBridgeError(payload.get("error", "Bridge request failed"))
        return payload

    def ping(self) -> bool:
        try:
            self.request("ping")
            return True
        except GridBridgeError:
            return False

    def state(self) -> dict[str, Any]:
        return self.request("state")

    def capabilities(self) -> dict[str, Any]:
        return self.request("capabilities")

    def inspect(self) -> dict[str, Any]:
        return self.request("inspect")

    def set_parameters_atomic(self, parameters: dict[int, float]) -> dict[str, Any]:
        assignments = " ".join(
            f"{int(index)}={float(value) / 128.0}" for index, value in parameters.items()
        )
        return self.request(f"batch {assignments}")
    def set_parameter(self, index: int, value: float) -> dict[str, Any]:
        return self.request(f"set {index} {value / 128.0}")

    def set_parameters(self, parameters: dict[int, float]) -> dict[str, Any]:
        for index, value in parameters.items():
            self.set_parameter(index, value)
        return {"ok": True, "changed": list(parameters)}
