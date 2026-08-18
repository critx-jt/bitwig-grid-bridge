#!/usr/bin/env python3
"""Small, dependency-free demonstrations of the Bitwig Grid bridge.

Open one of the example projects in Bitwig before running this script. The
bridge must be enabled and listening on 127.0.0.1:8765.
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import time
from collections.abc import Sequence

BRIDGE_HOST = os.environ.get("BITWIG_GRID_BRIDGE_HOST", "127.0.0.1")
BRIDGE_PORT = int(os.environ.get("BITWIG_GRID_BRIDGE_PORT", "8765"))
FX_GRID_UUID = "d641f61b-d4db-4006-930e-cdd7aeb3e9d7"


class BridgeError(RuntimeError):
    """Raised when the bridge rejects a request."""


class BridgeClient:
    """Minimal client for the bridge's line-oriented JSON protocol."""

    def __init__(self, host: str = BRIDGE_HOST, port: int = BRIDGE_PORT) -> None:
        self.address = (host, port)

    def request(self, command: str) -> dict:
        try:
            with socket.create_connection(self.address, timeout=3.0) as connection:
                connection.sendall(f"{command}\n".encode("utf-8"))
                response = connection.makefile("r", encoding="utf-8").readline()
        except OSError as error:
            raise BridgeError(f"bridge unavailable at {self.address}: {error}") from error
        payload = json.loads(response)
        if not payload.get("ok", False):
            raise BridgeError(payload.get("error", "bridge request failed"))
        return payload


def emit(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def inspect(client: BridgeClient) -> None:
    emit(client.request("capabilities"))
    emit(client.request("inspect"))
    emit(client.request("state"))


def graph(client: BridgeClient) -> None:
    """Print live graph capability and state when the device exposes it."""
    capabilities = client.request("graph-capabilities")
    emit(capabilities)
    if capabilities.get("graph_available"):
        emit(client.request("graph-state"))




def sweep(client: BridgeClient, index: int, minimum: float, maximum: float, steps: int,
          duration: float, keep: bool) -> None:
    if not 1 <= index <= 8:
        raise ValueError("index must be between 1 and 8")
    if not 0 <= minimum <= maximum <= 1:
        raise ValueError("minimum and maximum must be normalized values in [0, 1]")
    if steps < 2:
        raise ValueError("steps must be at least 2")

    before = client.request("state")
    original = next(
        parameter["value"]
        for parameter in before["parameters"]
        if parameter["index"] == index
    )
    interval = duration / (steps - 1)
    try:
        for step in range(steps):
            position = step / (steps - 1)
            value = minimum + (maximum - minimum) * position
            emit(client.request(f"set {index} {value:.6f}"))
            if step + 1 < steps:
                time.sleep(interval)
    finally:
        if not keep:
            emit(client.request(f"set {index} {original:.6f}"))


def insert_fx_grid(client: BridgeClient, position: str, keep: bool) -> None:
    emit(client.request(f"insert {position} {FX_GRID_UUID}"))
    time.sleep(0.2)
    emit(client.request("inspect"))
    if not keep:
        emit(client.request("undo"))
        time.sleep(0.2)
        emit(client.request("inspect"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("inspect", help="print bridge, container, and remote-control state")
    subparsers.add_parser("graph", help="print graph capabilities and live graph state")
    sweep_parser = subparsers.add_parser("sweep", help="animate one exposed remote control")
    sweep_parser.add_argument("--index", type=int, default=2, help="remote-control index (1-8)")
    sweep_parser.add_argument("--minimum", type=float, default=0.2, help="normalized start value")
    sweep_parser.add_argument("--maximum", type=float, default=0.8, help="normalized end value")
    sweep_parser.add_argument("--steps", type=int, default=16)
    sweep_parser.add_argument("--duration", type=float, default=3.0, help="seconds for the sweep")
    sweep_parser.add_argument("--keep", action="store_true", help="do not restore the original value")

    insert_parser = subparsers.add_parser("insert-fx-grid", help="insert the Bitwig FX Grid device")
    insert_parser.add_argument("--position", choices=("before", "after"), default="after")
    insert_parser.add_argument("--keep", action="store_true", help="keep the inserted device")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    client = BridgeClient()
    if args.command == "inspect":
        inspect(client)
    elif args.command == "graph":
        graph(client)
    elif args.command == "sweep":
        sweep(client, args.index, args.minimum, args.maximum, args.steps, args.duration, args.keep)
    elif args.command == "insert-fx-grid":
        insert_fx_grid(client, args.position, args.keep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
