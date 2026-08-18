# Agent integration reference

This section is for MCP clients, scripts, and orchestration layers. It defines
the supported transport, startup contract, tool entry points, and safety gates.
For producer-facing procedures, use the [Producer guide](../index.md).

## Supported integration path

```text
MCP client or example script
        │ MCP stdio or local bridge protocol
        ▼
Python MCP adapter (optional)
        │ newline-delimited JSON over 127.0.0.1:8765
        ▼
Bitwig Grid Bridge extension
        │ serialized host-thread calls
        ▼
Bitwig Controller API 21+
```

The Java extension is authoritative. The Python adapter is a thin MCP surface;
it does not infer state or reconstruct graph topology.

The former OSC compatibility transport is deprecated, disabled by default, and
not started by the MCP adapter. Existing direct OSC modules remain only for
legacy callers; new integrations must use the Grid Bridge endpoint.

## Start the adapter

From a source checkout or release bundle:

```bash
uv sync --frozen
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run bitwig-mcp
```

Example MCP client configuration:

```json
{
  "mcpServers": {
    "bitwig-grid-bridge": {
      "command": "uv",
      "args": ["run", "--project", "/absolute/path/to/bitwig-grid-bridge", "bitwig-mcp"],
      "cwd": "/absolute/path/to/bitwig-grid-bridge",
      "env": {
        "BITWIG_MCP_GRID_BRIDGE_ENABLED": "true",
        "BITWIG_MCP_GRID_BRIDGE_HOST": "127.0.0.1",
        "BITWIG_MCP_GRID_BRIDGE_PORT": "8765"
      }
    }
  }
}
```

The adapter keeps stdout reserved for MCP messages. Capture logs through the
client's stderr facility.

## Startup contract

1. The extension is enabled in Bitwig.
2. The adapter pings `127.0.0.1:8765`.
3. Startup succeeds only after the bridge responds.
4. No UDP socket or legacy compatibility listener is required.
5. A bridge error is returned as an unavailable service, not as inferred state.

## First calls

Every session should begin with:

```text
get_grid_capabilities
get_selected_device_state
```

If the capability response reports `graph_available: false`, do not call graph
inspection or mutation tools. Selected-device inspection and exposed-control
operations may still be available.

## Reference pages

- [Workflow playbook](workflows.md): safe end-to-end tool sequences and completion evidence.
- [Tool reference](tools.md): MCP names, arguments, and mutation classes.
- [Data and safety](models.md): snapshots, identities, ranges, and revisions.
- [Protocol and lifecycle](protocol.md): transport and recovery invariants.
- [Automation scripts](../scripting.md): direct bridge use without MCP.
