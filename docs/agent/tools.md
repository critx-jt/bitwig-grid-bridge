# Tool reference

Tool names are the MCP contract. Arguments use JSON objects. Read tools do not
mutate Bitwig. Graph, device, and shaping apply tools require explicit
`confirm: true` or an explicitly authorized `cooperative: true` argument.

Use the [Workflow playbook](workflows.md) for safe ordering, state refreshes,
verification, and recovery.

## Read tools

| Tool | Arguments | Result |
| --- | --- | --- |
| `get_grid_capabilities` | `{}` | Bridge capabilities and selected-device inspection flags. |
| `get_selected_device_state` | `{}` | Current selected device, exposed parameters, and optional graph. |
| `get_grid_graph` | `{}` | Live modules, ports, connections, coordinates, and parameters. |
| `get_grid_host_modulators` | `{}` | Host modulation sources for the selected Grid. |
| `search_grid_modules` | `{"query": "..."}` | Installed module catalog matches. |
| `search_grid_modulators` | `{"query": "..."}` | Semantic modulator catalog matches. |
| `grid_list_tracks` | `{}` | Live main-track bank and zero-based indexes. |
| `grid_soundscape_plan` | `{"brief": "..."}` | Non-mutating generic recipe. |
| `grid_list_soundscape_styles` | `{}` | Generic style vocabulary. |
| `grid_list_style_presets` | `{}` | Authored shaping profiles. |
| `grid_shape_status` | `{"session_id": "..."}` | Current preview and revision. |

## Preview-first shaping

```json
{"brief":"sparse evolving bed","style":"deep-bed"}
```

Call `grid_shape_start`, then optionally `grid_shape_compose`, and inspect the
returned preview. Apply only the exact current revision:

```json
{
  "session_id": "grid-...",
  "revision": 2,
  "confirm": true
}
```

Use `grid_shape_undo` with the session ID to restore the previous applied
revision.

## Graph and device mutations

| Tool | Required arguments | Confirmation |
| --- | --- | --- |
| `grid_insert_module` | `package_id`, `x`, `y` | required |
| `grid_set_module_parameter` | `module_id`, `parameter_id`, `value` | required |
| `grid_connect_modules` | source/target module and port indexes | required |
| `grid_disconnect_module` | `target_module_id`, `target_port` | required |
| `grid_insert_modulator` | `package_id`, `x`, `y` | required |
| `grid_set_modulator_parameter` | `module_id`, `parameter_id`, `value` | required |
| `grid_connect_modulator` | source/target module and port indexes | required |
| `grid_insert_device` | `position`, `device_id` | required |
| `set_selected_device_parameters` | `parameters` map | call is mutating; confirm at orchestration layer |
| `grid_select_track` | `track_index` from `grid_list_tracks` | selection change |
| `grid_navigate_device` | `direction`: `next`, `previous`, or `parent` | selection change |

Graph coordinates are Grid points. Package IDs come from the live catalog;
instance IDs and port indexes come from the current graph snapshot.

## Recovery tools

- `grid_shape_undo`: undo the latest applied shaping revision.
- `grid_project_undo`: undo the latest Bitwig host operation.
- `grid_project_redo`: redo the latest Bitwig host operation.
- `save_parameter_snapshot`: capture process-local selected-device values.
- `compare_parameter_snapshots`: compare two named snapshots.
- `apply_parameter_snapshot`: restore a named snapshot.

## Error handling

A failed call returns MCP text beginning with `Error:`. Treat it as a failed
operation. Re-read state before retrying. Never retry a mutation with stale
selection, revision, package ID, or port indexes.
