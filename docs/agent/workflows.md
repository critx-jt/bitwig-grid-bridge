# Agent workflow playbook

This page defines safe tool sequences for MCP agents. The [Tool reference](tools.md) remains the source of exact input schemas.

## Mandatory opening sequence

Begin every independent task with:

1. `get_grid_capabilities({})`
2. `get_selected_device_state({})`
3. `get_grid_graph({})` only when `graph_available` is `true` and graph structure is relevant.

Do not treat a successful MCP connection as proof that graph tools are available. Do not reuse selected-device state, graph revisions, instance IDs, or track indexes from another task or session.

Summarize the observed target and proposed single change before mutation. If the user did not already authorize a mutation, request confirmation at the orchestration layer and pass `confirm: true` only after authorization.

## Classify the request

| User intent | Preferred path | Mutation gate |
| --- | --- | --- |
| Inspect, explain, compare current state | capability and state reads | none |
| Draft a sound or interaction | `grid_soundscape_plan` or shaping preview | none until apply |
| Tune exposed controls | snapshot, parameter batch, read-back | orchestration confirmation |
| Shape from a brief | start, compose, apply exact revision | `confirm: true` on apply |
| Insert or cable a Grid module | live catalog, graph, one mutation, fresh graph | `confirm: true` per mutation |
| Add or tune modulation | live modulator catalog and graph | `confirm: true` per mutation |
| Navigate tracks/devices | list, select/navigate, re-read | selection changes immediately |
| Recover a bad edit | session undo, snapshot restore, or host undo | match recovery to change |

`cooperative: true` is for an explicitly authorized cooperative prompt or active skill. It is not a substitute for inferred consent.

## Read-only inspection

For “what is selected?” or “explain this patch”:

1. Read capabilities.
2. Read selected-device state.
3. If graph access is available, read the graph.
4. Describe only returned modules, ports, parameters, coordinates, connections, and current values.
5. Distinguish live state from catalog metadata.

If `graph_available` is false, say that graph inspection is unavailable for the selected device. Continue with exposed controls when those answer the question; never reconstruct a graph from names or UI assumptions.

## Preview-first shaping

A safe shaping session is revision-bound:

```json
{"brief":"less density, slow movement, preserve the low end","style":"slow-air"}
```

1. Optionally call `grid_list_style_presets({})` and `grid_list_soundscape_styles({})`.
2. Call `grid_shape_start` with the brief and optional style, preset, intensity, or explicit controls.
3. Present the returned preview. Name material parameter changes and the audible intention.
4. If refinement is requested, call `grid_shape_compose` with the returned `session_id` and the changed shaping inputs.
5. Present the new preview and record its latest `revision`.
6. Apply only that revision:

```json
{"session_id":"...","revision":2,"confirm":true}
```

7. Call `grid_shape_status` and then `get_selected_device_state` to verify the applied result.
8. Offer `grid_shape_undo` only for this session's latest applied revision.

A stale revision rejection is final for that attempt. Read current state and compose a new revision; do not force or replay the old apply.

## Exposed-parameter A/B workflow

Use snapshots when the user wants a reversible parameter experiment:

1. Read selected-device state and identify exact indexes.
2. `save_parameter_snapshot({"name":"before"})`
3. Apply the authorized batch with `set_selected_device_parameters`.
4. Read state and verify returned values.
5. Optionally `save_parameter_snapshot({"name":"candidate"})`.
6. `compare_parameter_snapshots({"first":"before","second":"candidate"})`
7. Keep the candidate or restore with `apply_parameter_snapshot({"name":"before"})`.
8. Read state again.

Values use the bridge's 0–128 exposed-parameter range. Do not pass normalized 0–1 values to this tool.

Snapshots are process-local and selected-device-specific in practice. Do not assume they survive an adapter restart or remain applicable after selection changes.

## Insert one Grid module

1. Confirm `graph_available: true`.
2. Search with `search_grid_modules({"query":"..."})`.
3. Resolve one exact package ID from the returned live catalog.
4. Read the current graph and select free coordinates.
5. Call `grid_insert_module` with `package_id`, integer `x`/`y` in the supported coordinate range, and `confirm: true`.
6. Read the graph again.
7. Identify the inserted instance by the new live instance ID, not by package name alone.
8. Stop and report the insertion, or continue to a separately reviewed connection step.

An insertion response does not authorize a cable mutation. Dependent edits need the fresh graph because IDs and layout can change.

## Connect two modules

1. Read the graph immediately before the change.
2. Resolve source module instance, source output index, target module instance, and target input index.
3. Verify that the target input is the intended destination and inspect any current connection.
4. Call `grid_connect_modules`:

```json
{
  "source_module_id":"...",
  "source_port":0,
  "target_module_id":"...",
  "target_port":1,
  "confirm":true
}
```

5. Read the graph and verify the exact connection exists.
6. Stop if any identifier or port is absent. Never guess an index from module documentation or another instance.

To remove a route, use `grid_disconnect_module` with the live target module ID and target port. Re-read afterward.

## Tune a native module parameter

1. Read the graph.
2. Find the module instance and parameter record.
3. Use its returned `id`, `type`, native `range`, or discrete `options`.
4. Call `grid_set_module_parameter` with the native number or boolean and `confirm: true`.
5. Read the graph and verify the value.

Display strings are not necessarily valid native values. If the response does not define a label-to-value mapping, do not invent one.

## Add or connect a modulator

1. Search `search_grid_modulators` for catalog candidates.
2. Read `get_grid_host_modulators` and `get_grid_graph`.
3. Insert one modulator with `grid_insert_modulator` if needed.
4. Re-read the graph to get its live instance ID and parameter metadata.
5. Tune with `grid_set_modulator_parameter` using the native contract.
6. Connect with `grid_connect_modulator` using live source and target port indexes.
7. Re-read and verify.

Keep insertion, tuning, and connection as distinct mutations with fresh state between them.

## Insert a device around the selection

`grid_insert_device` requires a known Bitwig device UUID and `position` equal to `before` or `after`.

1. Read selected-device state.
2. Resolve the device UUID from an authoritative catalog or user-provided value.
3. Insert once with explicit confirmation.
4. Re-read selected-device state and navigate only if needed.
5. If the wrong host operation occurred, use `grid_project_undo` after confirming no unrelated operation intervened.

Never substitute a display name for the required UUID.

## Navigate to another target

1. Call `grid_list_tracks({})`.
2. Select using the returned zero-based index: `grid_select_track({"track_index": N})`.
3. Read selected-device state.
4. Navigate with `grid_navigate_device({"direction":"next"})`, `previous`, or `parent`.
5. Read selected-device state after every navigation.

Selection is shared with the user. If the selected device differs from the expected target, stop and establish intent instead of continuing a stale plan.

## Recovery selection

| Change made | Recovery tool | Constraint |
| --- | --- | --- |
| Applied shaping revision | `grid_shape_undo` | same shaping `session_id` |
| Exposed parameter batch | `apply_parameter_snapshot` | named in-memory snapshot still valid |
| Latest graph/device host edit | `grid_project_undo` | no unrelated host operation intervened |
| Wrong undo | `grid_project_redo` | confirm the undone operation first |

Always read state after recovery. An undo response is not enough to infer the selected device, graph revision, or audible outcome.

## Error and timeout policy

All MCP tool calls return text content. A payload beginning with `Error:` is a failed operation even though the MCP transport call itself completed.

On any failed or ambiguous mutation:

1. Stop the sequence.
2. Do not retry with the old payload.
3. Read capabilities and current state from a new observation point.
4. Determine whether the mutation applied.
5. Re-plan with current IDs, revision, selection, and ranges.

A timeout is ambiguous: Bitwig may have completed the host operation before the response was lost. Automatic mutation retries can duplicate devices, modules, cables, or parameter changes.

## Completion evidence

A task is complete only when the agent can report:

- the exact target observed before mutation;
- the tool and authorized arguments used;
- the state or graph read after mutation;
- the intended observable difference;
- the available recovery action;
- any capability boundary that limited the result.

For audible work, the final judgment belongs to the user listening in Bitwig. State read-back proves control state, not sound quality.
