# Installation

Install the Bitwig extension first. Add the optional Python MCP adapter only when a local agent needs to use the bridge.

## Requirements

- Bitwig Studio with Controller API 21 or newer
- A local account able to write to the Bitwig Extensions directory
- Python 3.10 or newer and `uv` for the optional MCP adapter
- Java 21 and Maven only when building the extension from source

The runtime bridge binds to loopback only at `127.0.0.1:8765`. It claims no MIDI ports and requires no external hardware.

## Install from a GitHub release

Download either the standalone `BitwigGridBridge.bwextension` asset or the `bitwig-grid-bridge-VERSION.zip` bundle from the latest GitHub release.

### Standalone extension

Copy `BitwigGridBridge.bwextension` into the user extensions directory:

```bash
mkdir -p "$HOME/Bitwig Studio/Extensions"
cp BitwigGridBridge.bwextension "$HOME/Bitwig Studio/Extensions/"
```

On Windows, use the Bitwig Studio Extensions folder under the current user's Documents directory.

Restart Bitwig, open **Settings → Controllers**, add **Bitwig Grid Bridge**, and enable it.

### Full bundle

Extract the bundle and follow `INSTALL.txt`. It contains:

- the ready-to-install `.bwextension`;
- the optional Python adapter source and locked environment;
- Python wheel and source distribution under `python/`;
- documentation, automation examples, sample projects, and MCP client configuration;
- Java extension source for optional rebuilding.

From the extracted bundle:

```bash
uv sync --frozen
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run bitwig-mcp
```

The adapter should log that the Bitwig Grid Bridge connected at `127.0.0.1:8765`.

## Build from source

Clone the repository, then build and install the Java extension:

```bash
mvn -f extension/pom.xml package
mkdir -p "$HOME/Bitwig Studio/Extensions"
cp extension/target/BitwigGridBridge.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
```

The equivalent repository command is:

```bash
make install-extension
```

Restart Bitwig after replacing the extension file.

### Optional Maven usage

Maven is not required when installing the release `.bwextension`. Use it only for source development:

```bash
make build-extension
```

The stable output path is `extension/target/BitwigGridBridge.jar`.

## Verify the extension

Open a project, select a device, and run from a source checkout or bundle:

```bash
python examples/automation/grid_bridge_demo.py inspect
```

A healthy response contains `"ok": true` and current selected-device data.

For a supported selected Grid:

```bash
python examples/automation/grid_bridge_demo.py graph
```

If the response reports `graph_available: false`, the connection is healthy but graph operations are unavailable for that selection. Select the intended Grid or use exposed-control workflows.

## Install the optional MCP adapter

From a checkout or full bundle:

```bash
uv sync --frozen
```

Start the adapter only after Bitwig and the extension are running:

```bash
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run bitwig-mcp
```

`uv run python -m bitwig_mcp_server` remains equivalent. The `bitwig-mcp` console command is included in built Python distributions.

Example MCP client configuration:

```json
{
  "mcpServers": {
    "bitwig-grid-bridge": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--project", "/absolute/path/to/bitwig-grid-bridge", "bitwig-mcp"],
      "cwd": "/absolute/path/to/bitwig-grid-bridge",
      "env": {
        "BITWIG_MCP_GRID_BRIDGE_ENABLED": "true",
        "BITWIG_MCP_LOG_LEVEL": "WARNING"
      },
      "timeout": 120000
    }
  }
}
```

Use an absolute path. The adapter fails fast if the bridge is unavailable; it does not silently fall back to OSC.

## Upgrade

1. Stop the MCP adapter.
2. Replace `BitwigGridBridge.bwextension` with the new release asset.
3. Restart Bitwig.
4. Update the checkout or bundle used by the Python adapter.
5. Run `uv sync --frozen`.
6. Start the adapter and read capabilities again.

Do not carry graph revisions, instance IDs, snapshot names, or shaping sessions across an upgrade.

## Troubleshooting

### Extension does not appear

- Confirm the filename ends in `.bwextension`.
- Confirm it is in the current user's Bitwig Extensions directory.
- Restart Bitwig after copying it.
- Inspect Bitwig's controller-extension log for Java loading errors.
- Confirm the release targets Controller API 21 and the installed Bitwig version supports it.

### Bridge unavailable at startup

- Confirm Bitwig is running and **Bitwig Grid Bridge** is enabled.
- Run the direct `inspect` command before starting MCP.
- Confirm no second Bitwig instance or stale process owns port `8765`.
- Keep host and port at the defaults unless the extension and adapter are changed together.

### MCP client times out

Run the adapter manually from a terminal. A healthy process stays open and logs a successful Grid Bridge connection. A process that exits with “bridge unavailable” has correctly rejected startup; fix the extension or port rather than increasing the MCP client timeout.

### OSC controller is installed but MCP still fails

OSC is not the supported MCP transport. Install and enable **Bitwig Grid Bridge**. Legacy OSC classes are opt-in compatibility code and do not satisfy the adapter startup check.
