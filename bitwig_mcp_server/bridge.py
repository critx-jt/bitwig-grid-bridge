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
            with socket.create_connection(
                (self.host, self.port), self.timeout
            ) as connection:
                connection.sendall((command + "\n").encode("utf-8"))
                response = connection.makefile("r", encoding="utf-8").readline()
        except OSError as error:
            raise GridBridgeError(
                f"Bridge unavailable at {self.host}:{self.port}: {error}"
            ) from error
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
            f"{int(index)}={float(value) / 128.0}"
            for index, value in parameters.items()
        )
        return self.request(f"batch {assignments}")

    def graph_capabilities(self) -> dict[str, Any]:
        return self.request("graph-capabilities")

    def graph_state(self) -> dict[str, Any]:
        return self.request("graph-state")

    def graph_host_modulators(self) -> dict[str, Any]:
        return self.request("graph-host-modulators")

    def graph_catalog(self, query: str = "") -> dict[str, Any]:
        command = "graph-catalog" if not query else f"graph-catalog {query}"
        return self.request(command)

    def graph_modulators(self, query: str = "") -> dict[str, Any]:
        command = "graph-modulators" if not query else f"graph-modulators {query}"
        return self.request(command)

    def graph_insert_modulator(self, package_id: str, x: int, y: int) -> dict[str, Any]:
        return self.request(f"graph-insert-modulator {package_id} {int(x)} {int(y)}")

    def graph_connect_modulator(
        self,
        source_module_id: str,
        source_port: int,
        target_module_id: str,
        target_port: int,
    ) -> dict[str, Any]:
        return self.request(
            f"graph-connect-modulator {source_module_id} {int(source_port)} "
            f"{target_module_id} {int(target_port)}"
        )

    def graph_set_modulator_parameter(
        self, module_id: str, parameter_id: str, value: float | int | bool
    ) -> dict[str, Any]:
        if isinstance(value, bool):
            encoded = str(value).lower()
        else:
            encoded = str(float(value))
        return self.request(f"graph-set-modulator {module_id} {parameter_id} {encoded}")

    def graph_insert(self, package_id: str, x: int, y: int) -> dict[str, Any]:
        return self.request(f"graph-insert {package_id} {int(x)} {int(y)}")

    def graph_set_parameter(
        self, module_id: str, parameter_id: str, value: float | int | bool
    ) -> dict[str, Any]:
        if isinstance(value, bool):
            encoded = str(value).lower()
        else:
            encoded = str(float(value))
        return self.request(f"graph-set {module_id} {parameter_id} {encoded}")

    def graph_connect(
        self,
        source_module_id: str,
        source_port: int,
        target_module_id: str,
        target_port: int,
    ) -> dict[str, Any]:
        return self.request(
            f"graph-connect {source_module_id} {int(source_port)} "
            f"{target_module_id} {int(target_port)}"
        )

    def graph_disconnect(
        self, target_module_id: str, target_port: int
    ) -> dict[str, Any]:
        return self.request(f"graph-disconnect {target_module_id} {int(target_port)}")

    def history(self) -> dict[str, Any]:
        return self.request("history")

    def actions(self, filter_text: str = "") -> dict[str, Any]:
        command = "actions" if not filter_text else f"actions {filter_text}"
        return self.request(command)

    def invoke_action(self, action_id: str) -> dict[str, Any]:
        return self.request(f"action {action_id}")

    def insert_device(self, position: str, device_id: str) -> dict[str, Any]:
        return self.request(f"insert {position} {device_id}")

    def undo(self) -> dict[str, Any]:
        return self.request("undo")

    def redo(self) -> dict[str, Any]:
        return self.request("redo")

    def navigate(self, direction: str) -> dict[str, Any]:
        if direction not in {"next", "previous", "parent"}:
            raise ValueError(f"Unsupported device navigation: {direction}")
        return self.request(direction)

    def tracks(self) -> dict[str, Any]:
        return self.request("tracks")

    def select_track(self, index: int) -> dict[str, Any]:
        return self.request(f"track {int(index)}")


    def set_parameter(self, index: int, value: float) -> dict[str, Any]:
        return self.request(f"set {index} {value / 128.0}")

    def set_parameters(self, parameters: dict[int, float]) -> dict[str, Any]:
        for index, value in parameters.items():
            self.set_parameter(index, value)
        return {"ok": True, "changed": list(parameters)}
