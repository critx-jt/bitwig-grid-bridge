# Bitwig Grid Bridge installation

Bitwig Grid Bridge is the Bitwig-side automation extension. The Python MCP
adapter is optional and uses the bridge when available.

## Requirements

- Bitwig Studio with controller API 21 or newer
- Java 21 or newer
- Maven
- Python 3.10+ and `uv` for the optional MCP adapter

## Build and install the extension

From the repository root:

```bash
mvn -f extension/pom.xml package
cp extension/target/bitwig-grid-bridge-0.1.0.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
```

Restart Bitwig, open **Settings > Controllers**, add **Bitwig Grid Bridge**, and
enable it. The extension binds only to `127.0.0.1:8765` and claims no MIDI
ports.

## Optional OSC controller

The Python adapter retains OSC fallback support. If OSC is needed, configure
Bitwig's **Generic > Open Sound Control** controller with:

- Remote host: `127.0.0.1`
- Remote send port: `9000`
- Remote listen port: `8000`
- SLIP: disabled

The MCP startup path does not wait for an OSC `/refresh` response. Binding the
receive socket is the startup health check; `/refresh` is best effort.

## Optional MCP adapter

```bash
uv sync
BITWIG_MCP_GRID_BRIDGE_ENABLED=true python -m bitwig_mcp_server
```

The bridge settings use the `BITWIG_MCP_` prefix:

```text
BITWIG_MCP_GRID_BRIDGE_ENABLED=true
BITWIG_MCP_GRID_BRIDGE_HOST=127.0.0.1
BITWIG_MCP_GRID_BRIDGE_PORT=8765
```

The MCP tools currently expose selected-device state, Grid container
inspection, remote-control batches, and snapshots. The local bridge protocol
also supports device insertion, navigation, application actions, and undo/redo.

## Showcase projects

Open a disposable project from the repository's `examples/` directory before
running the automation demo:

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py sweep --index 2 --duration 4
python examples/automation/grid_bridge_demo.py insert-fx-grid --position after
```

`sweep` restores its original value unless `--keep` is supplied. Device
insertion is undone by default. Use the checked-in project copies rather than
an active music project.

## Capability boundary

The bridge does not expose Grid modules, ports, cables, coordinates, or graph
mutation. `graph_available: false` is an explicit capability result, not a
temporary fallback. Arbitrary graph automation requires a supported Bitwig
graph API or a separate version-gated serializer validated against disposable
project copies.
