# Bitwig Grid Bridge architecture

Bitwig Grid Bridge has two layers:

```text
Agent / MCP client
        │
        ▼
Optional Python MCP + OSC adapter
        │ 127.0.0.1:8765
        ▼
Bitwig Grid Bridge controller extension
        │ Bitwig Controller API 21
        ▼
Selected device / container / remote controls
```

The Java extension is the live-control boundary. The Python layer is an
optional transport adapter; it prefers the bridge for selected-device
operations and retains OSC fallback for older controls.

## Extension responsibilities

The extension:

- Owns the loopback TCP listener.
- Subscribes to selected-device and remote-control state.
- Schedules every Bitwig API read and write through `ControllerHost`.
- Applies parameter batches in one host task.
- Exposes device insertion points, device navigation, application actions, and
  undo/redo.
- Returns explicit capability and error responses.

The local protocol is newline-delimited JSON. Each request is a single command,
and each response is one JSON object. The listener binds to `127.0.0.1` only;
it is not a network control surface.

## Threading and concurrency

Socket clients run on daemon worker threads. Workers never access Bitwig API
objects directly. They call `host.scheduleTask`, wait for completion, and
serialize the result as JSON.

This gives the bridge a simple cooperative-agent contract:

- State reads may be concurrent.
- Bitwig mutations are serialized by the host task queue.
- A parameter batch is one mutation unit.
- Agents still need a higher-level per-project writer/lease policy to prevent
  semantic conflicts between independently selected devices.

The Python adapter retries bridge discovery when the extension starts after the
MCP process. A bridge error disables the bridge path for the current request
and preserves OSC fallback.

## MCP integration

The Python MCP adapter currently exposes:

- `get_grid_capabilities`
- `get_selected_device_state`
- `set_selected_device_parameters`
- Parameter snapshot/compare/apply tools

The bridge protocol additionally supports deterministic insertion, navigation,
application actions, and undo/redo. These commands should be surfaced through
allowlisted MCP tools only after adding project identity and expected-state
preconditions.

## Capability boundary

`graph_available: false` is intentional. The public Bitwig controller API does
not expose:

- Grid module instances
- Module ports or cables
- Grid coordinates
- Graph serialization or mutation

The bridge must not infer those structures from OSC addresses, UI selection
state, or undocumented native `.bwproject`/`.bwpreset` bytes. Arbitrary Grid
generation requires a supported Bitwig graph API or a separately version-gated
serializer validated against disposable project copies.

## Recommended agent transaction envelope

Before adding broader mutation commands, wrap bridge operations in a
coordinator-owned envelope containing:

```json
{
  "request_id": "unique-id",
  "project": "expected-project-name",
  "selected_device": "expected-device-identity",
  "expected_revision": 42,
  "dry_run": false,
  "operation": "set_selected_device_parameters"
}
```

The coordinator should serialize writes, reject stale selection/revision
preconditions, report the exact changed indexes, and provide an explicit undo
boundary for each agent transaction.
