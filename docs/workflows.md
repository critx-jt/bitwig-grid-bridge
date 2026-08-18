# Workflows

Use one visible goal per session. Every live operation follows the same
checkpoint sequence:

1. **Observe** capabilities, selection, and current values.
2. **Plan** the single change and expected result.
3. **Preview** when a non-mutating step exists.
4. **Apply** one confirmed mutation.
5. **Verify** by reading the new state.
6. **Recover** with undo or a snapshot when needed.

Keep a disposable project open while learning. It is valid to stop after any
read-only step.

## Preview-first shaping

Use shaping when you have a sound or interaction brief and exposed controls on
the selected device:

```text
1. get_grid_capabilities
2. get_selected_device_state
3. grid_shape_start(brief, style or preset)
4. grid_shape_compose(session_id, changes)
5. grid_shape_status(session_id)
6. Review the before → after preview
7. grid_shape_apply(session_id, revision, confirm=true)
8. grid_shape_status(session_id)
```

Rules:

- A preview does not change Bitwig.
- A shaping draft uses normalized `0..1` values; the bridge applies the exposed
  control values.
- The exact current revision is required for apply.
- If selection changed, re-read and compose again.
- Use `grid_shape_undo` to restore the previous applied shaping state.

### Choose a starting style

| Style | Starting character |
| --- | --- |
| `glass` | bright, open, precise motion |
| `ember` | warm, body-forward motion |
| `acid` | high-contrast rhythmic motion |
| `hollow` | sparse, airy space |

Authored profiles provide a more specific starting direction:
`slow-air`, `deep-bed`, `distant-events`, `soft-drift`, `night-motion`,
`layered-motion`, and `pulse-lab`.

Change one control at a time after the first preview. Leave headroom instead of
filling every control.

## Inspecting and editing a Grid graph

Start only when `get_grid_capabilities` reports `graph_available: true`.

```text
1. get_grid_capabilities
2. get_grid_graph
3. search_grid_modules or search_grid_modulators
4. Resolve the package ID or live instance ID
5. Insert, connect, or edit one item with confirmation
6. Re-read get_grid_graph
7. Verify parameters from live range/options metadata
```

Do not reuse instance IDs, port indexes, coordinates, or package assumptions
from another project. Re-read after selection, insertion, connection, or reload.

### Keep a graph readable

For a layout another person can inspect:

- keep the primary signal around `y=2`;
- keep modulation around `y=4` or `y=5`;
- keep secondary voice/effect modules around `y=7`;
- leave roughly three Grid points between adjacent modules;
- keep a typical graph within `x=2..29`, `y=2..7` when possible.

A coordinate-only move may not survive reload in the current Bitwig build. For a
persistent relayout, capture the graph, clear and reinsert modules at explicit
positions, reconnect routes, restore writable parameters, save, restart, and
verify.

## Remote controls and snapshots

For a small reversible experiment:

```bash
python examples/automation/grid_bridge_demo.py sweep \
  --index 2 --minimum 0.2 --maximum 0.8 --duration 4
```

The example restores the original value unless `--keep` is supplied.

For a larger edit:

1. Save a named parameter snapshot.
2. Make one change or preview.
3. Compare the snapshots.
4. Restore the first snapshot when needed.
5. Read the selected-device state again.

## Navigation

Use the live track list and bridge navigation tools:

```text
grid_list_tracks
grid_select_track(track_index)
grid_navigate_device(direction="next" | "previous" | "parent")
```

Re-read selected-device state after navigation. A device name is not a durable
identity across containers or projects.
