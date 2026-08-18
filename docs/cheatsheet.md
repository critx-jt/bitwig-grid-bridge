# Cheat sheet

Copy the smallest block that matches the task. Read state before every live
change.

## Install and verify

```bash
make install-extension
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py graph
```

For a release asset, copy `BitwigGridBridge.bwextension` directly instead of
running Maven.

## Start the optional MCP adapter

```bash
uv sync --frozen
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run bitwig-mcp
```

The MCP configuration, exact tool contracts, and safe sequences are in the
[agent reference](agent/index.md) and [agent workflow playbook](agent/workflows.md).

## Read and preview

```text
get_grid_capabilities
get_selected_device_state
grid_shape_start(brief="...")
grid_shape_compose(session_id="...", controls={...})
grid_shape_status(session_id="...")
```

## Apply and recover

```text
grid_shape_apply(session_id="...", revision=N, confirm=true)
grid_shape_status(session_id="...")
grid_shape_undo(session_id="...")
grid_project_undo
grid_project_redo
```

## Graph operations

All graph mutations require `confirm: true` or explicitly authorized
`cooperative: true`.

| Operation | Tool |
| --- | --- |
| Inspect capabilities | `get_grid_capabilities` |
| Read the graph | `get_grid_graph` |
| Find modules | `search_grid_modules` |
| Find modulators | `search_grid_modulators` |
| Insert a module | `grid_insert_module` |
| Set a module parameter | `grid_set_module_parameter` |
| Connect modules | `grid_connect_modules` |
| Disconnect an input | `grid_disconnect_module` |
| Undo/redo host work | `grid_project_undo`, `grid_project_redo` |

## Selected device

| Need | Tool |
| --- | --- |
| Navigate device | `grid_navigate_device` |
| List tracks | `grid_list_tracks` |
| Select a track | `grid_select_track` |
| Set exposed parameters | `set_selected_device_parameters` |
| Save a snapshot | `save_parameter_snapshot` |
| Compare snapshots | `compare_parameter_snapshots` |
| Restore a snapshot | `apply_parameter_snapshot` |

## Example commands

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py graph
python examples/automation/grid_bridge_demo.py sweep \
  --index 2 --minimum 0.2 --maximum 0.8 --duration 4
python examples/automation/grid_bridge_demo.py insert-fx-grid --position after
```

`sweep` restores the original value by default. `insert-fx-grid` undoes the
insertion by default. Add `--keep` only when you intend to retain a change.

## Common messages

| Message | Action |
| --- | --- |
| Bridge unavailable at `127.0.0.1:8765` | Enable the extension and restart Bitwig. |
| `graph_available: false` | Use selected-device workflows only. |
| `confirm must be true` | Review the mutation and pass explicit confirmation. |
| `stale draft revision` | Read status and compose a new revision. |
| Selected device changed | Re-read state; do not write from a stale snapshot. |
| Unexpected result | Use the matching undo or restore a named snapshot. |
