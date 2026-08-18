# Bitwig Grid Bridge

Bitwig Grid Bridge is a Bitwig Studio controller extension and automation
toolkit for agents. It exposes a small, deterministic local API for selected
devices, Grid containers, remote controls, device insertion, application
actions, and undo/redo.

The repository is intentionally bridge-first. The Python MCP server remains as
a companion adapter for agent clients; the Bitwig extension is the source of
truth for host-thread scheduling and live device control.

## Supported automation surface

- Inspect the selected device and container slots.
- Read the eight remote controls exposed by Bitwig.
- Apply multiple remote-control values in one host-thread batch.
- Navigate selected devices and parent containers.
- Insert Bitwig devices by UUID.
- Invoke allowlisted Bitwig application actions.
- Inspect project history and use undo/redo.
- Connect multiple local clients without concurrent Bitwig API access.

The bridge does **not** expose Grid modules, ports, cables, coordinates, or
arbitrary graph mutation. `graph_available: false` is intentional. Do not
infer a Grid graph from OSC addresses or edit native `.bwproject`/`.bwpreset`
binary data in a live project.

## Requirements

- Bitwig Studio with controller API 21 or newer.
- Java 21 or newer and Maven.
- Python 3.10+ and `uv` for the optional MCP adapter.

## Install the Bitwig extension

```bash
git clone https://github.com/critx-jt/bitwig-grid-bridge.git
cd bitwig-grid-bridge

mvn -f extension/pom.xml package
cp extension/target/bitwig-grid-bridge-0.1.0.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
```

Restart Bitwig, then enable **Bitwig Grid Bridge** under
**Settings > Controllers**. The extension listens only on
`127.0.0.1:8765`; it does not claim MIDI ports or external hardware.

## Run the optional MCP adapter

The existing Python adapter translates MCP calls to the bridge and retains OSC
fallback support for controls that are not bridge-backed.

```bash
uv sync
BITWIG_MCP_GRID_BRIDGE_ENABLED=true python -m bitwig_mcp_server
```

The default bridge settings are:

```text
BITWIG_MCP_GRID_BRIDGE_HOST=127.0.0.1
BITWIG_MCP_GRID_BRIDGE_PORT=8765
```

## Showcase projects

The checked-in projects under [`examples/`](examples/) are disposable Bitwig
fixtures:

- `polygrid-remote-controls` demonstrates selected Poly Grid inspection and
  reversible remote-control sweeps.
- `polygrid-fx-chain` demonstrates deterministic FX Grid insertion and undo.

Open one project in Bitwig, enable the extension, then run:

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py sweep --index 2 --duration 4
python examples/automation/grid_bridge_demo.py insert-fx-grid --position after
```

The sweep restores the original value by default. Device insertion is also
undone by default; pass `--keep` to commit either operation. Use the copied
example projects rather than an active music project.

## Repository layout

```text
extension/                 Bitwig controller extension and local protocol
examples/                  Disposable Bitwig projects and automation demos
bitwig_mcp_server/         Optional MCP/OSC adapter and bridge client
tests/                     Python adapter and protocol regression tests
docs/                      Architecture and installation notes
```

## Development

```bash
# Build the extension
mvn -f extension/pom.xml package

# Run focused Python checks
uv run pytest tests/test_bridge.py tests/osc/test_controller.py -q
uv run ruff check bitwig_mcp_server tests/test_bridge.py tests/osc/test_controller.py

# Build documentation
uv run mkdocs build --strict
```

## Design boundary

For cooperative agents, allow concurrent reads but serialize mutations through
one per-project writer. Add selected-device identity, expected-state revisions,
idempotency keys, dry-run responses, and explicit undo boundaries before
exposing more mutation commands.

Arbitrary Grid graph generation requires a supported Bitwig graph API or a
separate, version-gated serializer validated against disposable project
copies. Until then, use trusted example projects and preset/template workflows.
