# Grid automation examples

These projects are disposable Bitwig fixtures for bridge demonstrations. Copy a
project directory into your Bitwig Projects folder or open its `.bwproject`
file directly.

| Project | What it demonstrates |
| --- | --- |
| `projects/polygrid-remote-controls` | Read a selected Poly Grid and sweep one exposed remote control atomically. |
| `projects/polygrid-fx-chain` | Select a Poly Grid and insert an FX Grid by Bitwig device UUID, with undo support. |

## Dependency-free bridge script

With Bitwig running and **Bitwig Grid Bridge** enabled:

```bash
# Read capabilities, selected device, container, and remote controls.
python examples/automation/grid_bridge_demo.py inspect

# Read graph capabilities and live graph state when exposed.
python examples/automation/grid_bridge_demo.py graph

# Sweep remote control 2 and restore its original value.
python examples/automation/grid_bridge_demo.py sweep \
  --index 2 --minimum 0.2 --maximum 0.8 --duration 4

# Insert an FX Grid, inspect it, then undo the insertion.
python examples/automation/grid_bridge_demo.py insert-fx-grid --position after
```

The script uses `127.0.0.1:8765` by default. Override the endpoint with
`BITWIG_GRID_BRIDGE_HOST` and `BITWIG_GRID_BRIDGE_PORT`.

`sweep` restores the original value unless `--keep` is supplied. Device
insertion is also reversible by default; pass `--keep` only when you intend to
leave the change in the project. Run all commands against a checked-in copy,
not an active music project.

## Oh My Pi composition recipes

The `compositions/` directory contains briefs for the interactive shaping tools:

```text
compositions/glass-aperture.json
compositions/ember-pulse.json
compositions/style-presets.json
```

Start `/grid-shape` in Oh My Pi with a recipe's `brief`, then use its `preset`,
`style`, `intensity`, and named `controls` as the preview target. The recipe
files describe starting compositions; they are not binary project patches.

## What the examples prove

The examples intentionally cover the supported surface:

- selected-device and exposed remote-control state;
- container inspection and stable live navigation;
- device insertion by UUID;
- graph capability and live graph inspection when available;
- reversible changes and undo.

They do not claim arbitrary graph mutation from OSC or from a project file. For
MCP graph insertion, connection, and parameter workflows, use the
[documentation workflows](../docs/workflows.md) and the live capability response
as the authority.
