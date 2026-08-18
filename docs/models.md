# Models and boundaries

The bridge has a small set of observable models. Treat each response as a
snapshot of the current Bitwig session, not as a permanent identifier map.

## Capability model

`get_grid_capabilities` is the first gate for graph work.

| Field | Meaning |
| --- | --- |
| `graph_available` | The selected device exposes the version-gated Grid graph surface. |
| `graph_inspection` | Module, port, parameter, and coordinate reads are available. |
| `module_catalog` | Installed Grid package IDs can be resolved. |
| `module_insertion` | A known package can be inserted at explicit coordinates. |
| `port_connections` | Graph input/output connections can be inspected and changed. |
| `native_undo` | Bitwig host undo/redo is available through the bridge. |

When `graph_available` is false, stop graph work. Do not infer topology from
OSC, pixels, names, or native project-file bytes.

## Selected-device model

A selected-device snapshot describes the current host target:

```text
project → track → device/container path → selected device
                                     └── exposed parameters
                                     └── remote controls
                                     └── optional Grid graph
```

Selection can change outside the MCP session. Re-read before each mutation and
reject stale assumptions.

## Grid graph model

A graph snapshot contains:

- `modules.items`: the current module instances;
- `instance_id`: an identifier valid for this project state;
- `package_id`: the installed module package UUID used for insertion;
- `module_name`: the runtime display name;
- `x`, `y`: Grid-point coordinates;
- `inputs` and `outputs`: ports with indexes and names;
- `connection`: the source module and source port for a connected input;
- `parameters`: native type, current value, range, and/or discrete options.

A port index is local to its module. Never reuse an index after rebuilding or
reselecting a graph without re-reading the graph.

## Parameter model

Parameters expose one of these useful shapes:

```json
{"id": "GAIN", "type": "float", "value": -6.0,
 "range": {"min": -24.0, "max": 24.0}}
```

```json
{"id": "MODEL", "type": "integer",
 "options": [{"label": "Analog", "value": 0},
             {"label": "Digital", "value": 2}]}
```

```json
{"id": "RETRIGGER", "type": "boolean", "value": true}
```

Use the native range or option values. Do not assume every numeric parameter is
normalized; shaping sessions normalize their own exposed-control draft, while
Grid graph parameters use the live native base-value domain.

## Mutation authorization

Mutating MCP tools accept:

- `confirm: true` for an explicit user-confirmed operation;
- `cooperative: true` only when the prompt or active skill explicitly authorizes
  cooperative mutation.

Without one of these flags, mutation is rejected. A successful tool response is
not a substitute for a verification read.

## Shaping session model

A shaping session is process-local and contains:

| Field | Meaning |
| --- | --- |
| `session_id` | Short-lived identifier for the preview session. |
| `brief` | Human intent in sensory or interaction terms. |
| `preset` / `style` | Parameter scaffold and authored behavior profile. |
| `intensity` | Blend amount in `0..1`. |
| `draft` | Pending normalized control values. |
| `revision` | Monotonic preview revision required by apply. |
| `baseline` | Selected-device state captured at session start. |
| `history` | Applied changes available to session undo. |

Sessions are not project files and do not contain hidden preset payloads.

## Identity and lifetime rules

- Package UUIDs describe installed catalog entries.
- Instance IDs describe modules in one live graph.
- Coordinates describe one saved graph layout.
- Track indexes describe one live track-bank view.
- Session IDs describe one running MCP process.

Re-read the relevant model after selection, insertion, connection, navigation,
or restart.
