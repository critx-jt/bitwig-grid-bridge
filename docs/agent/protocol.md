# Protocol and lifecycle

The extension owns the authoritative local protocol. It accepts one newline
delimited command and returns one JSON object per request on loopback.

## Request path

1. The MCP adapter validates the tool name and arguments.
2. The adapter checks mutation authorization.
3. The bridge resolves the live selected device or catalog entry.
4. The extension schedules host-thread work as one operation.
5. The extension returns a structured success or error object.
6. The adapter converts the result to MCP text content.
7. The caller reads state again when the operation mutates Bitwig.

The extension serializes Bitwig API access. It does not resolve conflicting
intent between agents; coordinate writers above the bridge.

## Endpoint

- Host: `127.0.0.1`
- Port: `8765`
- Protocol: newline-delimited JSON commands and responses
- Scope: local machine only

The deprecated OSC compatibility listener is not part of this lifecycle and is
not started by the MCP adapter.

## Capability boundary

The Java bridge uses the available in-process Grid access and reports its
capabilities explicitly. `graph_available: false` means:

- graph topology is unavailable;
- graph coordinates and ports must not be inferred;
- graph mutation must not be attempted;
- selected-device and exposed-control operations may still work.

## Persistence and recovery

Shaping sessions and revisions are process-local. Graph and device operations
use host undo/redo. Named parameter snapshots cover parameter-only recovery.

In the current Bitwig build, a coordinate-only graph move can report success
without surviving reload. A persistent relayout therefore requires:

```text
snapshot → clear → insert at explicit coordinates → reconnect
→ restore parameters → save → restart → verify
```

Keep that sequence behind explicit confirmation and one undo boundary.
