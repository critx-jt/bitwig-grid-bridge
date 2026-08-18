# Workflows

Bitwig Grid Bridge is designed around small, observable steps. Read first,
change one thing, verify, and keep an undo boundary visible.

## The standard transaction

Use this sequence for every live operation:

1. **Observe** — read capabilities, selected-device identity, and current state.
2. **Plan** — name the intended change and the expected result.
3. **Preview** — use a non-mutating tool or recipe when one exists.
4. **Apply** — make one confirmed mutation.
5. **Verify** — read state again; compare the result with the plan.
6. **Recover** — undo or restore a snapshot if the result is not expected.

This sequence is deliberately repetitive. Predictability is a feature.

## Preview-first shaping

Use this for exposed selected-device controls and artistic briefs:

```text
1. get_grid_capabilities
2. get_selected_device_state
3. grid_shape_start(brief, style or preset)
4. grid_shape_compose(session_id, changes)
5. grid_shape_status(session_id)
6. Review the returned before → after preview
7. grid_shape_apply(session_id, revision, confirm=true)
8. grid_shape_status(session_id)
```

Rules:

- Controls are normalized to `0..1` in the shaping session.
- A style is a starting vocabulary, not a finished sound.
- Applying an old revision is rejected.
- If the selected device changed externally, re-read and re-compose.
- `grid_shape_undo` restores the previous applied session state.

### Built-in style vocabulary

| Style | Use it for | Default character |
| --- | --- | --- |
| `glass` | bright, open, precise voices | light motion and shimmer |
| `ember` | warm, body-forward voices | restrained movement |
| `acid` | high-contrast rhythmic material | assertive motion |
| `hollow` | sparse, airy beds | low density and space |

Authored profiles add a conservative intensity and compositional principle:
`slow-air`, `deep-bed`, `distant-events`, `soft-drift`, `night-motion`,
`layered-motion`, and `pulse-lab`.

## Inspecting and editing a Grid graph

Graph operations are available only when `get_grid_capabilities` reports
`graph_available: true`.

```text
1. get_grid_capabilities
2. get_grid_graph
3. search_grid_modules or search_grid_modulators
4. Resolve the returned package ID
5. Insert or connect one module with explicit confirmation
6. Re-read get_grid_graph
7. Set parameters from the live range/options metadata
8. Re-read get_grid_graph again
```

Do not infer module IDs, port indexes, coordinates, or package names from a
previous project or from OSC addresses. Instance IDs and coordinates belong to
the current project state.

### Persistent placement

Use compact lanes when laying out a graph for a human to inspect:

- primary signal lane: `y=2`;
- modulation/control lane: `y=4` or `y=5`;
- secondary voice/effect lane: `y=7`;
- adjacent modules: about 3 Grid points apart;
- compact target for a typical graph: `x=2..29`, `y=2..7`.

In the current Bitwig build, coordinate-only `graph-move` can report success
without surviving a reload. For a persistent relayout, use a complete snapshot,
then clear and reinsert the modules at explicit positions, reconnect every route,
restore writable parameters, save, and verify after restarting Bitwig.

## Remote controls and snapshots

For a single exposed remote control, the example script is intentionally small:

```bash
python examples/automation/grid_bridge_demo.py sweep \
  --index 2 --minimum 0.2 --maximum 0.8 --duration 4
```

The original value is restored unless `--keep` is supplied. For larger edits:

1. `save_parameter_snapshot(name)`
2. make one change or preview
3. `compare_parameter_snapshots(first, second)`
4. `apply_parameter_snapshot(name)` when restoration is needed

## Device navigation

Use stable live indexes, not guessed names:

```text
grid_list_tracks
grid_select_track(track_index)
grid_navigate_device(direction="next" | "previous" | "parent")
```

Re-read selected-device state after navigation. A device name is not a stable
identity across containers or projects.

## Multi-agent safety

The extension serializes Bitwig API access, but it does not resolve semantic
conflicts between agents. A coordinator should provide:

- one writer per project;
- selected-device identity;
- expected-state revision;
- idempotency key;
- explicit dry-run/preview result;
- one undo boundary per transaction.

Concurrent reads are safe to schedule; concurrent mutations need coordination.
