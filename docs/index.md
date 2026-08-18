# Bitwig Grid Bridge

Bitwig Grid Bridge is a local Bitwig Studio extension for inspecting devices,
shaping exposed controls, and working with supported Grid graphs. The site is
written for producers: start with a working project, make one visible change,
and keep an undo path.

## Start with a goal

| You want to… | Start here |
| --- | --- |
| Install the bridge | [Installation](installation.md) |
| Make the first connection | [Quickstart](quickstart.md) |
| Shape a sound from a brief | [Workflows](workflows.md#preview-first-shaping) |
| Inspect or edit a Grid graph | [Graph workflow](workflows.md#inspecting-and-editing-a-grid-graph) |
| Find a command quickly | [Cheat sheet](cheatsheet.md) |
| Connect an MCP client | [Agent reference](agent/index.md) |

## The working method

Use the same short sequence for every live change:

1. **Observe** the selected device and available capabilities.
2. **Plan** one intended change and its expected result.
3. **Preview** the change when a preview is available.
4. **Apply** one confirmed mutation.
5. **Verify** the new state in Bitwig.
6. **Recover** with undo or a saved snapshot if the result is wrong.

A read-only inspection is a complete stopping point. Save only when the result
is intentional.

## What the extension provides

- Selected-device, container, track, and project-history inspection.
- Eight exposed remote controls with atomic host-thread writes.
- Device navigation, device insertion, and host undo/redo.
- Grid module search, insertion, graph inspection, port connections, and
  parameter writes when the running extension reports those capabilities.
- Preview-first shaping sessions with styles, revisions, explicit confirmation,
  and session undo.
- A loopback-only local bridge at `127.0.0.1:8765`.

The capability response is authoritative. If `graph_available` is false, use
selected-device controls only. Do not infer graph modules, ports, coordinates,
or connections from another project or from the interface.

## Five-minute check

From the repository root:

```bash
mvn -f extension/pom.xml package
cp extension/target/bitwig-grid-bridge-0.1.0.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
python examples/automation/grid_bridge_demo.py inspect
```

Run the command after enabling **Bitwig Grid Bridge** in **Settings →
Controllers**. Use a copy of one of the projects in
[Examples](https://github.com/critx-jt/bitwig-grid-bridge/tree/main/examples)
while learning.

## Next step

Choose one small action from [Workflows](workflows.md). Keep the project open,
read the result, and stop before starting a second unrelated change.
