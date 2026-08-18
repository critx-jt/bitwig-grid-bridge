# Bitwig Grid Bridge

Bitwig Grid Bridge is a local Bitwig Studio extension and optional MCP adapter
for inspectable, reversible automation. It connects agents to the selected
device, exposed controls, and—when supported by the running extension—Grid
module graphs.

!!! tip "Start with the smallest path"
    Use the extension and an example script first. Add the MCP adapter only
    when an agent client needs it.

## What it does

- Reads selected-device, container, track, and project-history state.
- Controls exposed remote parameters in host-thread batches.
- Navigates devices and invokes allowlisted Bitwig actions.
- Inserts known Bitwig devices and Grid modules by runtime UUID.
- Inspects Grid modules, ports, coordinates, connections, and parameters when
  `graph_available` is true.
- Provides semantic modulator search and host-modulator inspection.
- Provides preview-first Grid shaping with revisions, confirmation, and undo.
- Keeps the Java bridge loopback-only and the Python MCP adapter optional.

## Choose a starting page

| Need | Page |
| --- | --- |
| First successful connection | [Quickstart](quickstart.md) |
| Install the extension, MCP adapter, or OSC fallback | [Installation](installation.md) |
| Understand the data returned by tools | [Models and boundaries](models.md) |
| Make a safe change | [Workflows](workflows.md) |
| Look up tools, variables, and recovery | [Cheat sheet](cheatsheet.md) |
| Reduce context switching and working-memory load | [Accessible use](accessibility.md) |
| Understand threads, transports, and safety | [Architecture](architecture.md) |
| Browse installed Grid packages | [Live Grid inventory](grid-device-inventory.md) |
| Browse semantic modulation roles | [Grid modulator catalog](grid-modulator-catalog.md) |

## Five-minute verification

```bash
mvn -f extension/pom.xml package
cp extension/target/bitwig-grid-bridge-0.1.0.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"

# After enabling the extension in Bitwig:
python examples/automation/grid_bridge_demo.py inspect
```

The extension listens on `127.0.0.1:8765` and claims no MIDI ports or external
hardware. The optional MCP adapter uses stdio and prefers the bridge when
`BITWIG_MCP_GRID_BRIDGE_ENABLED=true`.

## Safety boundary

`get_grid_capabilities` is authoritative. If `graph_available` is false, do not
invent module IDs, ports, cables, coordinates, or graph edits from OSC, pixels,
or native project bytes. Read state before mutations, confirm live changes, and
verify after them.

## Examples and project fixtures

The repository's [example projects and scripts](https://github.com/critx-jt/bitwig-grid-bridge/tree/main/examples)
are throwaway fixtures. Use copies while learning; do not run experiments
against an active music project.
