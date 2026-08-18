# Installation

Install the extension first. Add the MCP adapter only if a local agent needs
the bridge.

| Piece | Use | Endpoint |
| --- | --- | --- |
| Bitwig Grid Bridge extension | Every bridge workflow | `127.0.0.1:8765` |
| Python MCP adapter | Agent and MCP clients | stdio |

The extension is the supported Bitwig transport. The former OSC compatibility
transport is deprecated, disabled by default, and is not part of the producer
workflow.

## Requirements

- Bitwig Studio with Controller API 21 or newer.
- Java 21 and Maven.
- Python 3.10 or newer and `uv` for the optional MCP adapter.

## Install the extension

From the repository root:

```bash
mvn -f extension/pom.xml package
mkdir -p "$HOME/Bitwig Studio/Extensions"
cp extension/target/bitwig-grid-bridge-0.1.0.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
```

Restart Bitwig, open **Settings → Controllers**, add **Bitwig Grid Bridge**, and
enable it. The extension binds to loopback only and claims no MIDI ports or
external hardware.

Verify it with a disposable example project:

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py graph
```

`graph` is read-only. It reports graph state only when the selected device and
running extension expose the version-gated graph surface.

## Install the MCP adapter

The adapter is optional. Install its locked environment with:

```bash
uv sync
```

Start it from the repository root:

```bash
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run python -m bitwig_mcp_server
```

Use the [agent reference](agent/index.md) for client configuration, tool
schemas, and state rules.

## Troubleshooting

### The extension does not appear

- Confirm the file ends in `.bwextension` and is in the Bitwig Extensions folder.
- Restart Bitwig after copying a new build.
- Check the Bitwig log for extension load errors.
- Confirm Maven used Java 21.

### Port `8765` is already in use

Identify and stop the old bridge process before retrying. Do not change the host
or port in only one component; the extension and adapter must agree.

### The MCP process starts but tools are unavailable

- Confirm the extension is enabled.
- Run `inspect` outside the MCP client.
- Launch the MCP command from the repository root.
- Confirm the client runs `uv run ... python -m bitwig_mcp_server`.

### `graph_available` is false

This is a capability boundary, not a connection failure. Use selected-device
and exposed-control workflows, or select a Grid device that the extension can
inspect. Do not infer graph data.

### A mutation is rejected

Read the returned error. Common causes are missing confirmation, an unauthorized
cooperative request, a stale revision, a missing package UUID, or an out-of-range
native parameter. Re-read state before trying again.
