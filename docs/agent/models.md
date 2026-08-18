# Data and safety

Treat every response as a snapshot of the current Bitwig session. IDs and
indexes are scoped to the live project state.

## Capability gate

`get_grid_capabilities` is the first call for graph work.

| Field | Meaning |
| --- | --- |
| `graph_available` | The selected device exposes the version-gated Grid graph surface. |
| `graph_inspection` | Module, port, parameter, and coordinate reads are available. |
| `module_catalog` | Installed Grid package IDs can be resolved. |
| `module_insertion` | A known package can be inserted at explicit coordinates. |
| `port_connections` | Graph connections can be inspected and changed. |
| `native_undo` | Host undo/redo is available through the bridge. |

When `graph_available` is false, stop graph work. Do not infer topology from
names, coordinates, pixels, project bytes, or any other stale source.

## Selected-device snapshot

A selected-device response describes:

```text
project → track → device/container path → selected device
                                     └── exposed parameters
                                     └── optional Grid graph
```

Selection can change outside the MCP process. Re-read before every mutation.

## Graph snapshot

`get_grid_graph` may contain:

- `modules.items`: current module instances;
- `instance_id`: an identifier valid for this project state;
- `package_id`: the installed package UUID used for insertion;
- `x`, `y`: Grid-point coordinates;
- `inputs` and `outputs`: local port indexes and names;
- `connection`: the source module and port for a connected input;
- `parameters`: native type, value, range, and/or discrete options.

Port indexes are local to a module. Re-read after insertion, connection,
navigation, reload, or any failed mutation.

## Parameter domains

Graph parameters use the native domain returned by live metadata:

```json
{"id":"GAIN","type":"float","value":-6.0,
 "range":{"min":-24.0,"max":24.0}}
```

```json
{"id":"MODEL","type":"integer",
 "options":[{"label":"Analog","value":0},{"label":"Digital","value":2}]}
```

Shaping drafts use normalized `0..1` values. Do not apply that assumption to
native graph parameters.

## Authorization and revisions

Mutating tools require `confirm: true`, or `cooperative: true` only when the
prompt or active skill explicitly authorizes cooperative mutation. A shaping
session also requires its exact monotonic `revision`. Successful mutation is
not verification; read state again.

## Identity lifetime

- Package UUID: installed catalog entry.
- Instance ID: module in one live graph.
- Port index: input/output position within one module snapshot.
- Track index: live track-bank position.
- Session ID: process-local shaping session.

Never persist these as universal identifiers.
