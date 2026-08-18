# Installation

The bridge has three local pieces. Install only what you need.

| Piece | Required for | Transport | Default endpoint |
| --- | --- | --- | --- |
| Bitwig Grid Bridge extension | Every bridge workflow | newline-delimited JSON over TCP | `127.0.0.1:8765` |
| Python MCP adapter | Agent/MCP clients | MCP stdio | process stdin/stdout |
| OSC fallback | Legacy OSC-only control | OSC/UDP | send `8000`, receive `9000` |

The MCP adapter prefers the extension. OSC is a compatibility path, not a
replacement for graph inspection.

## Requirements

- Bitwig Studio with Controller API 21 or newer.
- Java 21 and Maven.
- Python 3.10 or newer and `uv` for the MCP adapter.

## Install the extension

From the repository root:

```bash
mvn -f extension/pom.xml package
mkdir -p "$HOME/Bitwig Studio/Extensions"
cp extension/target/bitwig-grid-bridge-0.1.0.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
```

Restart Bitwig, open **Settings → Controllers**, add **Bitwig Grid Bridge**, and
enable it. The extension binds only to `127.0.0.1:8765`; it does not claim MIDI
ports or external hardware.

Verify it with a disposable example project:

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py graph
```

`graph` is read-only. It reports capabilities and graph state when the selected
device exposes the version-gated graph surface.

## Run the MCP adapter

Install the locked Python environment:

```bash
uv sync
```

Start the stdio server:

```bash
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run python -m bitwig_mcp_server
```

MCP client configuration:

```json
{
  "mcpServers": {
    "bitwig-grid-bridge": {
      "command": "uv",
      "args": ["run", "--project", ".", "python", "-m", "bitwig_mcp_server"],
      "env": {
        "BITWIG_MCP_GRID_BRIDGE_ENABLED": "true",
        "BITWIG_MCP_GRID_BRIDGE_HOST": "127.0.0.1",
        "BITWIG_MCP_GRID_BRIDGE_PORT": "8765"
      }
    }
  }
}
```

The adapter keeps stdout reserved for MCP messages. Configure application logs
through the client's stderr capture. Environment variables use the
`BITWIG_MCP_` prefix; see [the cheat sheet](cheatsheet.md#start-the-mcp-adapter).

## Configure OSC fallback

Use OSC only when the Java bridge is unavailable or a legacy OSC workflow is
required. In Bitwig's OSC controller, use:

- Remote host: `127.0.0.1`
- Remote send port: `9000`
- Remote listen port: `8000`
- SLIP: disabled

Then set:

```text
BITWIG_MCP_GRID_BRIDGE_ENABLED=false
BITWIG_MCP_BITWIG_HOST=127.0.0.1
BITWIG_MCP_BITWIG_SEND_PORT=8000
BITWIG_MCP_BITWIG_RECEIVE_PORT=9000
```

OSC does not provide the Java bridge's Grid graph capabilities. The server must
not wait for an OSC refresh acknowledgement during startup; UDP binding is the
available readiness check.

## Oh My Pi and other local agents

Point the MCP client at the stdio command above. Keep the bridge and Bitwig on
the same machine unless you have a deliberate, authenticated tunnel; the
extension intentionally listens on loopback.

Give the agent this operating rule:

> Read capabilities and state, preview when possible, mutate one thing with
> explicit confirmation, then verify.

## Troubleshooting

### The extension does not appear

- Confirm the file ends in `.bwextension` and is in the Bitwig Extensions folder.
- Restart Bitwig after copying a new build.
- Check the Bitwig log for extension load errors.
- Confirm Java 21 was used by Maven.

### Port `8765` is already in use

Stop the old bridge/Bitwig process or identify the owner before retrying. Do
not change the documented port in one component only. The bridge and adapter
must use the same host and port.

### MCP starts but tools are unavailable

- Confirm the extension is enabled.
- Run the example `inspect` command outside the MCP client.
- Check that the MCP command's working directory is the repository root.
- Confirm the client launches `uv run ... python -m bitwig_mcp_server`.

### `graph_available` is false

This is a capability boundary, not a timeout. Use selected-device and exposed
remote-control tools, or select a Grid device that the running extension can
inspect. Do not infer graph data.

### A mutation is rejected

Read the returned error. Common causes are missing `confirm: true`, an
unauthorized cooperative request, a stale revision, a missing package UUID, or
an out-of-range native parameter. Re-read state before trying again.
