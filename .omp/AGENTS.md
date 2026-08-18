# Bitwig Grid Bridge

Use the `bitwig-grid-bridge` MCP server for live Bitwig interaction.

## Interaction contract

- Start with `get_grid_capabilities` and `get_selected_device_state`.
- Treat `graph_available: false` as a hard boundary. Never invent Grid modules,
  ports, cables, coordinates, or native project-file edits.
- For expressive shaping, use `grid_shape_start` → `grid_shape_compose` →
  `grid_shape_apply`. Preview output is non-mutating; apply requires the exact
  returned revision. Pass `cooperative: true` when the prompt or active skill
  explicitly requests cooperative work that includes the mutation; otherwise
  pass `confirm: true`.
- Explain the proposed changes as a small, legible diff before applying them.
- If the selected device or parameters changed outside the session, re-compose
  instead of overwriting the user's work.
- Use `grid_shape_undo` for session parameter rollback and
  `grid_project_undo`/`grid_project_redo` for host operations.
- Use `grid_insert_device` only with a known UUID and an explicit position.
  Pass `cooperative: true` for explicitly cooperative mutation requests;
  otherwise pass `confirm: true`.

## Inventory and graph modification

- Read `docs/grid-device-inventory.md` for the latest captured catalog and
  `docs/grid-device-inventory.json` for machine-readable package IDs.
- Treat the inventory as a reference snapshot; re-read live capabilities and
  graph state before every session mutation.
- Resolve module names with `search_grid_modules` and use the returned package
  UUID. Names such as `Sine`, `Ø Sine`, `Sawtooth`, `Pulse`, and `Triangle` are
  distinct catalog entries; do not substitute one for another.
- Re-read the graph after insertion, parameter, connection, or disconnection
  operations. Instance IDs and coordinates are project-state facts, not stable
  identifiers.
- Preserve existing routing unless the request explicitly asks for a
  replacement or connection. A newly inserted module may remain unconnected
  when that is the safest non-destructive interpretation.


## Grid placement

- Treat coordinates as Grid-point units, not pixels. Read live graph state
  before choosing positions and re-read it after every topology mutation.
- Use readable lanes: primary signal at `y=2`, secondary voice/effect paths at
  `y=7`, and modulation/control sources at `y=4` or `y=5`. Align shared
  endpoints vertically when a branch crosses lanes.
- Prefer approximately 3 Grid points between adjacent modules and approximately
  5 Grid points between signal lanes. Avoid the previous ruler-like 4-point
  spacing across the entire viewport; it creates excessive empty space.
- Keep compact sessions inside roughly `x=2..29`, `y=2..7` when the graph fits;
  reserve the remaining `40 × 20` viewport for future branches and inspection.
- `graph-move` can report success while its coordinate-only mutation does not
  survive a Bitwig reload in this build. For a requested persistent relayout,
  preserve a full snapshot, clear and reinsert modules at explicit coordinates,
  reconnect every route, restore writable parameters, save, and verify after
  restart.

## Style composition

Compose from a clear artistic brief: role, motion, density, contrast, and
emotional temperature. Prefer one of the built-in presets (`glass`, `ember`,
`acid`, `hollow`) or an authored style profile (`slow-air`, `deep-bed`,
`distant-events`, `soft-drift`, `night-motion`, `layered-motion`, `pulse-lab`)
as a starting vocabulary, then refine named controls in the 0-1 range. Keep
interaction staged: observe → compose → preview → apply → verify. Favor slow
evolution, bounded randomness, defined scales, layered roles, and deliberate
performance gestures over constant activity. Avoid a stream of unreviewed
parameter writes.

## `/grid-shape`

The project extension provides `/grid-shape <brief>` as a guided entry point.
Use it when the user wants an interactive shaping session rather than a single
parameter edit.
