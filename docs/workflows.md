# Producer workflows

Use the same short loop for every live change:

1. **Observe** the selected device and current capabilities.
2. **Plan** one audible or structural result.
3. **Preview** whenever the tool offers a preview.
4. **Apply** one confirmed mutation.
5. **Verify** by reading state and listening in Bitwig.
6. **Recover** immediately if the result is wrong.

Keep the Bitwig project open, keep the target track and device selected, and avoid changing selection in Bitwig while an operation is in progress. A selected-device name is not a durable identity.

## Inspect a Grid before editing

Start with `get_grid_capabilities`, then `get_selected_device_state`.

Check these fields before planning work:

- `graph_available`: whether the selected device exposes supported Grid graph operations.
- Selected-device name and type: whether the bridge is pointed at the intended device.
- Exposed controls and current values: the safe surface for parameter-only edits.
- Current graph revision and modules: the source of instance IDs, ports, and coordinates.

If `graph_available` is `false`, use exposed-control workflows only. Do not infer modules or cable routes from the Bitwig interface, screenshots, old inventory, or project files.

## Make a small parameter change

Use this path for an audible adjustment that does not alter the Grid graph.

1. Call `get_selected_device_state`.
2. Identify the exposed control by its returned index and current value.
3. Save a recovery point with `save_parameter_snapshot`.
4. Change one or more values with `set_selected_device_parameters`.
5. Read the selected-device state again and listen.
6. If necessary, restore the named snapshot with `apply_parameter_snapshot`.

For A/B work, save two snapshots and use `compare_parameter_snapshots` before deciding which state to keep. Snapshots are process-local: restarting the MCP adapter clears them.

## Shape exposed controls from a brief

Shaping is the safest creative workflow because it separates preview from mutation.

1. Call `grid_list_style_presets` for authored profiles, or `grid_list_soundscape_styles` for broader vocabulary.
2. Start a session with `grid_shape_start`, supplying a concrete brief and optional style.
3. Review the returned proposed controls, values, explanation, `session_id`, and `revision`.
4. Refine with `grid_shape_compose` when the preview misses the brief. Each compose creates a new revision.
5. Apply only the latest reviewed revision with `grid_shape_apply`, passing explicit confirmation.
6. Call `grid_shape_status` and listen in Bitwig.
7. Use `grid_shape_undo` with the same session ID to restore the pre-apply values.

A useful brief describes audible intent rather than implementation: “slower motion, fewer bright transients, preserve the bass weight.” The bridge chooses only from controls actually exposed by the selected device.

Never apply an earlier revision after composing a newer one. If Bitwig selection or parameters changed outside the session, re-read state and start or compose a fresh revision.

## Insert and connect a Grid module

Graph edits require a supported selected Grid and live graph state.

1. Call `get_grid_graph` and note the graph revision, existing instance IDs, coordinates, ports, and connections.
2. Search the installed catalog with `search_grid_modules`.
3. Choose the exact returned package ID; names are not insertion identifiers.
4. Pick free coordinates from the current graph.
5. Call `grid_insert_module` with the package ID, coordinates, and explicit confirmation.
6. Read `get_grid_graph` again. Find the new instance ID and its live input/output port indexes.
7. Call `grid_connect_modules` using those returned IDs and indexes.
8. Re-read the graph and verify that the expected module and connection exist.
9. Listen before making another structural change.

Do not chain insertion, parameter changes, and cabling from one old graph snapshot. Each mutation can change instance IDs, coordinates, connections, or revision.

## Add modulation

Use `search_grid_modulators` for host modulators and `get_grid_host_modulators` to inspect the modulators available on the selected Grid.

A safe sequence:

1. Read the graph and host-modulator state.
2. Resolve the exact modulator package or live instance.
3. Insert with `grid_insert_modulator` when needed.
4. Re-read the graph to obtain the new instance and parameter IDs.
5. Set one modulator control with `grid_set_modulator_parameter`.
6. Connect it with `grid_connect_modulator` using live port indexes.
7. Re-read and listen for range, polarity, and rate problems.

Prefer one modulation route at a time. Confirm that the destination remains musically useful at the full modulation range before adding a second route.

## Replace a parameterized graph detail

For a known module parameter:

1. Read `get_grid_graph`.
2. Resolve the module instance and native parameter ID from that response.
3. Check the returned type, native range, or options.
4. Call `grid_set_module_parameter` with explicit confirmation.
5. Read the graph again and compare the returned current value.

Never convert a display label directly into a native value unless the live response defines that mapping. Integer choices, booleans, and floats have different contracts.

## Disconnect or remove a route safely

`grid_disconnect_module` disconnects the target input identified by a live target module ID and target port index.

Before disconnecting:

1. Read the graph and identify the exact connection.
2. Note the source and target so the route can be reconstructed.
3. Disconnect with explicit confirmation.
4. Re-read the graph and verify only the intended connection disappeared.
5. Use `grid_project_undo` if the wrong host operation was applied.

## Navigate tracks and devices

Selection-changing tools are useful, but selection is shared with the Bitwig interface.

1. Call `grid_list_tracks` and use its zero-based track indexes.
2. Select with `grid_select_track`.
3. Call `get_selected_device_state` to establish the new context.
4. Move with `grid_navigate_device` using `next`, `previous`, or `parent`.
5. Re-read selected-device state after every navigation.

Do not cache track or device positions across project edits. Track banks, nesting, and selection can change.

## Draft a soundscape before touching the project

`grid_soundscape_plan` is non-mutating. Give it a brief to obtain a staged recipe, then inspect current capabilities before translating any step into live operations.

Use this for exploratory prompts such as:

- “A restrained metallic pulse with movement every eight bars.”
- “A distant granular bed that leaves the center clear for vocals.”
- “A low, unstable drone with no abrupt level changes.”

The plan is guidance, not proof that packages or graph operations are available. Resolve every package through the live catalogs and every instance through the current graph.

## Recovery order

Use the narrowest recovery mechanism that matches the change:

1. `grid_shape_undo` for the latest applied shaping revision.
2. `apply_parameter_snapshot` for a named exposed-control state.
3. `grid_project_undo` for the latest Bitwig host mutation.
4. `grid_project_redo` only after confirming the undone operation was the intended one.

After any recovery call, read state again. Never assume that undo restored the selection or graph context expected by an earlier snapshot.

## Stop conditions

Stop instead of retrying when:

- a tool result starts with `Error:`;
- the selected device changed;
- the graph revision is stale;
- a package ID, instance ID, parameter ID, or port index is missing;
- `graph_available` is `false` for a graph operation;
- Bitwig or the bridge extension restarted;
- the requested change cannot be expressed through returned capabilities.

Re-establish capabilities and live state before continuing. Repeating a stale mutation is more dangerous than leaving a partial edit visible and recoverable.
