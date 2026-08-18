# Cheat sheet

Copy the smallest block that matches the task. Read state before mutation.

## Install and verify

```bash
mvn -f extension/pom.xml package
cp extension/target/bitwig-grid-bridge-0.1.0.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
uv sync
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py graph
```

## Start the MCP adapter

```bash
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run python -m bitwig_mcp_server
```

Default environment:

| Variable | Default | Purpose |
| --- | --- | --- |
| `BITWIG_MCP_GRID_BRIDGE_ENABLED` | `true` | Prefer the Java bridge. |
| `BITWIG_MCP_GRID_BRIDGE_HOST` | `127.0.0.1` | Bridge host. |
| `BITWIG_MCP_GRID_BRIDGE_PORT` | `8765` | Bridge port. |
| `BITWIG_MCP_BITWIG_HOST` | `127.0.0.1` | OSC host. |
| `BITWIG_MCP_BITWIG_SEND_PORT` | `8000` | OSC send port. |
| `BITWIG_MCP_BITWIG_RECEIVE_PORT` | `9000` | OSC receive port. |

## Read-only MCP tools

| Need | Tool |
| --- | --- |
| Bridge and graph support | `get_grid_capabilities` |
| Selected device and controls | `get_selected_device_state` |
| Full module graph | `get_grid_graph` |
| Installed module lookup | `search_grid_modules` |
| Semantic modulation lookup | `search_grid_modulators` |
| Host modulation sources | `get_grid_host_modulators` |
| Generic soundscape plan | `grid_soundscape_plan` |
| List soundscape vocabulary | `grid_list_soundscape_styles` |
| Authored shaping profiles | `grid_list_style_presets` |
| Tracks | `grid_list_tracks` |

## Preview-first shaping

```text
grid_shape_start(brief="...")
grid_shape_compose(session_id="...", controls={...})
grid_shape_status(session_id="...")
grid_shape_apply(session_id="...", revision=N, confirm=true)
grid_shape_status(session_id="...")
```

Undo the latest applied shaping revision with:

```text
grid_shape_undo(session_id="...")
```

## Graph operations

All graph mutations require `confirm: true` or explicitly authorized
`cooperative: true`.

| Operation | Tool |
| --- | --- |
| Insert cataloged modulator | `grid_insert_modulator` |
| Connect cataloged modulator | `grid_connect_modulator` |
| Set modulator parameter | `grid_set_modulator_parameter` |
| Insert known module | `grid_insert_module` |
| Set module parameter | `grid_set_module_parameter` |
| Connect any module ports | `grid_connect_modules` |
| Disconnect an input | `grid_disconnect_module` |
| Host undo/redo | `grid_project_undo`, `grid_project_redo` |

For graph edits: capabilities → graph → package/port resolution → one mutation
→ graph verification. Use native ranges and options from the live response.

## Device and transport controls

| Need | Tool |
| --- | --- |
| Play/pause | `transport_play` |
| Tempo | `set_tempo` |
| Track volume/pan/mute | `set_track_volume`, `set_track_pan`, `toggle_track_mute` |
| Navigate selected device | `grid_navigate_device` |
| Select a track | `grid_select_track` |
| Set selected-device parameters | `set_selected_device_parameters` |
| Save/compare/apply snapshot | `save_parameter_snapshot`, `compare_parameter_snapshots`, `apply_parameter_snapshot` |

## Example script

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py graph
python examples/automation/grid_bridge_demo.py sweep \
  --index 2 --minimum 0.2 --maximum 0.8 --duration 4
python examples/automation/grid_bridge_demo.py insert-fx-grid --position after
```

`sweep` restores the original value by default. `insert-fx-grid` undoes the
insertion by default. Add `--keep` only when you intend to retain the change.

## Undo and recovery

1. Re-read state.
2. Use `grid_shape_undo` for a shaping session.
3. Use `grid_project_undo` for the latest host graph/device operation.
4. Restore a named parameter snapshot when the change was parameter-only.
5. If state is ambiguous, stop and reopen the disposable project.

## Common errors

| Message or symptom | Action |
| --- | --- |
| Bridge unavailable at `127.0.0.1:8765` | Enable the extension and restart Bitwig. |
| `graph_available: false` | Use selected-device/remote-control tools only. |
| `confirm must be true` | Review the mutation and pass explicit confirmation. |
| `stale draft revision` | Re-run `grid_shape_status` or compose a new revision. |
| selected device changed | Re-read state; never overwrite from a stale snapshot. |
| OSC startup timeout | Check socket binding and use OSC only as fallback. |
