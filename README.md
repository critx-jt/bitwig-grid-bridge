# Bitwig Grid Bridge

Bitwig Grid Bridge is a local Bitwig Studio controller extension with an
optional Python MCP adapter. It provides an inspectable, reversible surface for
selected devices, exposed controls, and supported Grid graph operations.

**Producer documentation:**
[critx-jt.github.io/bitwig-grid-bridge](https://critx-jt.github.io/bitwig-grid-bridge/)

## Choose a path

| Goal | Reference |
| --- | --- |
| Install and use the bridge in Bitwig | [Producer quickstart](docs/quickstart.md) |
| Shape controls or edit a Grid graph | [Producer workflows](docs/workflows.md) |
| Connect Claude, Oh My Pi, or another MCP client | [Agent integration reference](docs/agent/index.md) |
| Implement an agent tool flow | [Agent tool reference](docs/agent/tools.md) |
| Contribute code | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Supported surface

- Selected-device, track, container, and project-history inspection.
- Eight exposed remote controls with atomic host-thread writes.
- Device navigation, insertion by UUID, and host undo/redo.
- Grid module catalog search, insertion, graph inspection, port connections,
  parameter writes, and native undo when the running extension exposes those
  capabilities.
- Semantic Grid modulator search and host-modulator inspection.
- Preview-first shaping sessions with styles, revisions, explicit mutation
  authorization, and session undo.
- Loopback-only local bridge at `127.0.0.1:8765`.

The capability response is authoritative. When `graph_available` is false,
graph topology must not be inferred from coordinates, UI pixels, stale state,
or native project bytes.

## Producer quickstart

### Prerequisites

- Bitwig Studio with Controller API 21 or newer.
- Java 21 and Maven.
- Python 3.10 or newer and `uv` for the optional MCP adapter.

### Build and install

```bash
mvn -f extension/pom.xml package
mkdir -p "$HOME/Bitwig Studio/Extensions"
cp extension/target/bitwig-grid-bridge-0.1.0.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
```

Restart Bitwig. Open **Settings → Controllers**, add **Bitwig Grid Bridge**, and
enable it.

### Verify before changing a project

Open a copy of a project from `examples/projects/`, select its Poly Grid, and
run:

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py graph
```

`graph` is read-only and returns graph state only when the selected device
exposes it.

### Make one safe change

Observe the current state, plan one result, preview when possible, apply one
confirmed mutation, and verify the new state. Keep undo available. See the
[Producer workflows](docs/workflows.md) for exact sequences.

## Optional MCP adapter

```bash
uv sync
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run python -m bitwig_mcp_server
```

The adapter uses MCP stdio and the local Grid Bridge endpoint. Its former OSC
compatibility transport is deprecated and disabled by default. Agent setup,
tool contracts, state lifetimes, and mutation gates are documented separately
in the [Agent reference](docs/agent/index.md).

## Examples

The [examples](examples/README.md) directory contains disposable Bitwig
projects, a dependency-free bridge client, and JSON composition recipes.
`inspect`, `graph`, and reversible `sweep`/`insert-fx-grid` commands demonstrate
the supported local protocol without requiring an agent.

## Development

```bash
uv sync
make check
make test
mvn -f extension/pom.xml package
```

`make check` runs the strict MkDocs build, Ruff, and the extension package build.
`make test` runs the focused Python regression suite. Integration tests that
need a live Bitwig session are separate.
