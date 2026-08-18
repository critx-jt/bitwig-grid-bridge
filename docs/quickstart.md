# Quickstart

This page gets a working local bridge in about ten minutes. Use the smallest
path that matches your goal.

| Goal | Start with |
| --- | --- |
| Control Bitwig without an agent | [Extension](installation.md#install-the-extension) + [example script](https://github.com/critx-jt/bitwig-grid-bridge/tree/main/examples) |
| Use Claude, Oh My Pi, or another MCP client | [MCP adapter](installation.md#run-the-mcp-adapter) |
| Explore Grid sound design safely | [Preview-first workflow](workflows.md#preview-first-shaping) |

## 1. Check prerequisites

You need:

- Bitwig Studio with Controller API 21 or newer.
- Java 21 and Maven for the extension.
- Python 3.10 or newer and `uv` for the optional MCP adapter.

No cloud account or external network service is required at runtime. The
bridge listens on loopback (`127.0.0.1`) only.

## 2. Build and install the extension

From the repository root:

```bash
mvn -f extension/pom.xml package
mkdir -p "$HOME/Bitwig Studio/Extensions"
cp extension/target/bitwig-grid-bridge-0.1.0.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
```

Restart Bitwig. Open **Settings → Controllers**, add **Bitwig Grid Bridge**,
and enable it.

## 3. Verify the bridge before adding an agent

Open a disposable project from `examples/projects/`, select its Poly Grid, then
run:

```bash
python examples/automation/grid_bridge_demo.py inspect
```

A healthy response includes `127.0.0.1:8765`, selected-device information, and
`ok: true`. If the graph capability is available, inspect the graph too:

```bash
python examples/automation/grid_bridge_demo.py graph
```

## 4. Start the MCP adapter

The adapter uses MCP stdio. Start it from the repository root:

```bash
uv sync
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run python -m bitwig_mcp_server
```

For an MCP client configuration, use the equivalent command:

```json
{
  "mcpServers": {
    "bitwig-grid-bridge": {
      "command": "uv",
      "args": ["run", "--project", ".", "python", "-m", "bitwig_mcp_server"],
      "env": {"BITWIG_MCP_GRID_BRIDGE_ENABLED": "true"}
    }
  }
}
```

The MCP process keeps the stdio channel open. Do not redirect its stdout to a
log file; use the client's stderr/log facility instead.

## 5. Make one safe change

Start with a read:

```text
get_grid_capabilities
get_selected_device_state
```

For exposed controls, use the preview-first sequence:

```text
grid_shape_start → grid_shape_compose → grid_shape_status
→ grid_shape_apply → grid_shape_status
```

`grid_shape_apply` requires the exact current revision and explicit
`confirm: true`, unless an explicitly cooperative workflow authorizes the
mutation. See [Workflows](workflows.md).

## If something fails

1. Stop after the first error; do not retry mutations blindly.
2. Confirm Bitwig is running and the extension is enabled.
3. Run `inspect` again.
4. Check whether `graph_available` is true before using graph tools.
5. Use a disposable project and [undo](cheatsheet.md#undo-and-recovery) before
   trying a different operation.

See [Installation and troubleshooting](installation.md) for port conflicts,
OSC fallback, and stale-state errors.
