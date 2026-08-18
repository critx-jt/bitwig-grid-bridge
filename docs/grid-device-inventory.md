# Generalized Grid device inventory

Schema **`grid-device-inventory.v2`**, revision **4** (`sha256-714cceb3dc62f9f30ad4e3e0492d02a73250532abe147673935835debeace0f4`). The interface catalog was captured from Bitwig Studio **6.0.11**. It is a reference snapshot, not a substitute for a live capability or graph read.

## Purpose and authority

`docs/grid-device-inventory.json` is a machine-readable package-interface inventory. It contains only information that can be reused when resolving and interfacing with a Grid module:

- installed package UUIDs and display names;
- input and output indexes and names;
- writable parameter IDs and native types;
- native numeric ranges and discrete option values.

The inventory deliberately excludes project state: instance IDs, coordinates, runtime classes and paths, connections, current parameter values, and display strings. Re-read `get_grid_capabilities` and `get_grid_graph` before every live operation. The bridge response is authoritative for the selected Bitwig installation.

If `graph_available` is false, do not infer modules, ports, cables, coordinates, or parameter metadata from this snapshot.

## File contract

| Field | Meaning |
| --- | --- |
| `schema_version` | Machine-readable schema identifier. |
| `inventory_revision` | Monotonic snapshot revision. |
| `revision_id` | SHA-256 of the canonical payload with `revision_id` set to `null`. |
| `bitwig_version` | Bitwig version used to capture the interface metadata. |
| `catalog` | Installed package UUID/name pairs suitable for module search and insertion. |
| `devices` | One generalized interface record per catalog package. |

Each `devices[]` record contains `name`, `package_id`, `inputs`, `outputs`, and `parameters`:

- Ports contain only `index` and `name`. Use the live graph for connection state.
- Parameters contain `id` and `type`, plus `range` for native numeric bounds when available.
- `options` contains accepted boolean or discrete values. Option-object labels are semantic choice names; they are not current-value labels.
- A parameter with neither `range` nor `options` has no safe static constraint metadata. Do not invent one; inspect the live graph before writing.

## Coverage

| Field | Count |
| --- | ---: |
| Installed catalog packages | 232 |
| Generalized package interfaces | 232 |
| Interface parameters | 873 |
| Numeric parameters with native ranges | 460 |
| Numeric parameters without native ranges | 115 |
| Boolean parameters with options | 298 |
| Discrete parameters with options | 102 |
| Parameters without static range/options metadata | 13 |
| Catalog packages missing an interface record | 0 |

## Interfacing workflow

1. Resolve a name with `search_grid_modules` and retain the returned `package_id`.
2. Use this inventory only to plan expected ports and writable parameter constraints.
3. Read `get_grid_capabilities`; stop graph work when graph access is unavailable.
4. Read `get_grid_graph` for current instance IDs, coordinates, ports, connections, values, ranges, and options.
5. Present a small before/after graph diff and use explicit confirmation for mutation.
6. Re-read the graph after insertion, parameter, connection, disconnection, or reload operations.

Package IDs are insertion identifiers. Instance IDs, coordinates, connections, and current values belong to the live project state and must never be reused from a reference snapshot.

## Revision and provenance

The revision ID is a SHA-256 digest of the JSON payload with `revision_id` set to `null`. Re-capture the inventory after a Bitwig upgrade, package change, or bridge protocol change. The inventory is intentionally project-independent; project names, graph placement, duplicate instances, and routing are not part of this file.
