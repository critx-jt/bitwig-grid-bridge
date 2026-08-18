# Automation scripts

The Java extension exposes a newline-delimited JSON protocol on loopback. Scripts can use it directly without starting the Python MCP adapter.

Use direct scripts for repeatable local procedures, development probes, and batch operations whose inputs are already known. Use the MCP adapter when an agent needs discoverable tools, validation, shaping sessions, snapshots, and consistent error responses.

## Prerequisites

1. Install and enable **Bitwig Grid Bridge** in Bitwig.
2. Keep Bitwig running with the target project open.
3. Confirm that `127.0.0.1:8765` is not occupied by another process.
4. Read capabilities and selected-device state before mutating anything.

The protocol is loopback-only. It has no remote transport, cloud service, or authentication layer.

## Run the included example

From a source checkout or release bundle:

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py graph
```

`inspect` works for any selected device and reports the exposed-control surface. `graph` requires a supported selected Grid.

The example also demonstrates reversible mutations:

```bash
python examples/automation/grid_bridge_demo.py sweep --index 2 --minimum 0.2 --maximum 0.8 --duration 4
python examples/automation/grid_bridge_demo.py insert-fx-grid --position after --keep
```

Omit `--keep` to let the example restore or undo its temporary change. Read the command output and verify the Bitwig state before running another operation.

## Protocol shape

Open a TCP connection to `127.0.0.1:8765`. Send one JSON object followed by a newline. Read one JSON object followed by a newline.

A request contains a command and optional arguments:

```json
{"command":"capabilities"}
```

```json
{"command":"selected_device_state"}
```

Successful and failed responses are explicit. A successful response contains `"ok": true`; a rejected request contains `"ok": false` and an error description. Treat a closed socket, malformed response, or missing `ok` field as failure.

Keep the exchange serialized: one request, one response. The extension schedules Bitwig API work on Bitwig's host thread before returning.

## Minimal Python client

```python
import json
import socket


def request(command: str, **arguments):
    with socket.create_connection(("127.0.0.1", 8765), timeout=3.0) as connection:
        stream = connection.makefile("rw", encoding="utf-8")
        stream.write(json.dumps({"command": command, **arguments}) + "\n")
        stream.flush()
        response = json.loads(stream.readline())
    if response.get("ok") is not True:
        raise RuntimeError(response.get("error", "bridge request failed"))
    return response


capabilities = request("capabilities")
state = request("selected_device_state")
print(capabilities)
print(state)
```

Open a new connection for a small one-off request, as above. A longer script may reuse one connection, but it must preserve request/response order and close the connection on any framing or timeout error.

## Safe script structure

A mutation script should have five explicit phases:

1. **Read** capabilities and current state.
2. **Validate** selected device, revision, IDs, indexes, and value ranges.
3. **Record** enough state to undo or restore the intended change.
4. **Mutate** once.
5. **Read back** and compare the observable result.

Do not turn a failed check into a warning and continue. A bridge rejection protects the user's project from stale or unsupported operations.

## Exposed-control automation

The selected-device response contains exposed parameter indexes and values. Those indexes belong to the current selected-device snapshot.

For sweeps or staged changes:

- clamp values to the returned bridge range;
- use a monotonic clock, not accumulated `sleep` durations, for timing;
- limit write frequency so Bitwig's host thread remains responsive;
- restore the original value in `finally` unless the caller explicitly asks to keep it;
- stop when selection or state no longer matches the initial target.

The included `sweep` example implements these guardrails. Prefer it over copying an unbounded write loop.

## Graph automation

Graph operations require `graph_available: true`. Each operation must use data from the latest graph response:

- package IDs from the live catalog;
- instance IDs from the live graph;
- native parameter IDs and types from the live graph;
- input and output indexes from the relevant module snapshot;
- coordinates from the current graph layout;
- the exact current graph revision when the command requires it.

After insertion, disconnection, parameter changes, or undo, request the graph again. Never issue a series of dependent graph mutations from the first snapshot.

## Long-running scripts

For a script that watches or changes Bitwig over time:

- use a bounded socket timeout;
- reconnect only for read-only probes;
- never automatically retry a mutation after an ambiguous timeout;
- log the request command, response status, selected-device identity, and revision;
- handle `SIGINT` and restore temporary parameter values where possible;
- rate-limit state reads and writes;
- exit when Bitwig or the bridge restarts instead of carrying stale IDs forward.

A timeout can occur after Bitwig applied a mutation but before the response reached the script. Re-read state and determine the outcome before any retry.

## When to wrap a script as an MCP workflow

Keep a script direct when it has a narrow, deterministic contract and an operator reviews its output. Add an MCP tool only when the operation needs to be discoverable and safely orchestrated by an agent.

An MCP-facing operation also needs:

- a precise JSON input schema;
- validation in the Python adapter and Java bridge;
- explicit mutation authorization;
- structured error mapping;
- tests for rejected and successful boundaries;
- producer and agent documentation;
- a recovery path.

See [Agent workflow playbook](agent/workflows.md) for orchestration patterns and [Engineering and releases](engineering.md) for implementation checks.

## Troubleshooting

### Connection refused

The extension is not listening. Confirm Bitwig is running, the extension is installed and enabled, and no stale Bitwig instance is holding the port. Restart Bitwig after replacing the extension file.

### Request times out

Stop the script. Do not retry a mutation. Check Bitwig's controller log, then run a read-only `capabilities` request from a fresh connection.

### `graph_available` is false

The connection is healthy, but the selected device does not expose the supported Grid graph surface. Select the intended Grid or use exposed-control commands.

### State changed during a run

Abort and re-read. Track selection, selected-device identity, graph revision, port indexes, and instance IDs are live state, not durable references.
