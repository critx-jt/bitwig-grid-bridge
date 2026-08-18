# Architecture

The bridge separates the agent-facing protocol from Bitwig's host-thread API.

```text
MCP client or example script
          │ stdio / TCP bridge protocol
          ▼
Python MCP + OSC adapter (optional)
          │ newline-delimited JSON over 127.0.0.1:8765
          ▼
Bitwig Grid Bridge extension
          │ serialized host-thread calls
          ▼
Bitwig Controller API 21 → selected device / Grid graph
```

## Transports

### Java bridge

The extension owns the authoritative local protocol. It binds to loopback only,
reads one JSON command per line, and emits one JSON object per request. It
serializes Bitwig calls through the host-thread scheduler and returns structured
errors instead of leaking host exceptions.

### Python MCP adapter

The adapter exposes MCP tools over stdio. It uses the Java bridge by default and
keeps OSC as a fallback for transport, mixer, and selected-device operations.
The adapter does not turn OSC addresses into graph topology.

## Request lifecycle

1. MCP dispatch validates the tool name and arguments.
2. The adapter checks mutation authorization.
3. The bridge resolves the live selected device or catalog entry.
4. Host-thread work runs as one scheduled operation.
5. The bridge returns a structured success/error response.
6. The adapter converts the response to MCP text content.
7. The caller reads state again when the operation mutates Bitwig.

The extension's executor is the concurrency boundary. It prevents simultaneous
Bitwig API calls, but it does not decide whether two agents have conflicting
intent. Coordinate writers above the bridge.

## Capability boundary

The Java adapter uses reflection to reach Bitwig's version-gated in-process Grid
model because the public Controller API does not expose arbitrary Grid graph
mutation. It reports capability failures explicitly. `graph_available: false`
means:

- no module or port topology is exposed;
- no graph coordinates should be inferred;
- no graph mutation should be attempted;
- selected-device and exposed-control tools may still work.

This boundary is intentional and should be preserved when adding features.

## State and identity

- Package UUIDs identify catalog entries installed in Bitwig.
- Instance IDs identify modules in the current graph.
- Port indexes are local to a module snapshot.
- Coordinates are Grid-point units, not pixels.
- Track indexes are live bank indexes, not durable IDs.
- Shaping sessions and revisions are process-local.

All are re-read after selection, insertion, connection, navigation, and restart.

## Mutations and recovery

Mutating MCP tools require explicit `confirm: true` or an explicitly authorized
`cooperative: true`. Shaping uses a revisioned draft and session undo. Graph and
device operations can use host undo/redo. Named parameter snapshots cover
parameter-only recovery.

A mutation is not complete when a call returns `ok`. The caller must verify the
new state and save only when the user intends the change to persist.

## Persistence caveat

In the current Bitwig build, coordinate-only graph moves can report success
without persisting after reload. Persistent layout changes therefore use:

```text
snapshot → clear → insert at explicit coordinates → reconnect
→ restore parameters → save → restart → verify
```

This is a runtime behavior, not a guarantee of the native API. Keep the
workflow behind explicit confirmation and an undo boundary.
