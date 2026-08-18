# Bitwig Grid Bridge

Bitwig Grid Bridge is a local Bitwig Studio controller extension with an
optional Python MCP adapter. It gives agents and scripts a small, inspectable,
reversible surface for selected devices, exposed controls, and supported Grid
graph operations.

**Documentation:** [critx-jt.github.io/bitwig-grid-bridge](https://critx-jt.github.io/bitwig-grid-bridge/)

## Choose a path

| You want to… | Use |
| --- | --- |
| Inspect or automate Bitwig directly | Java extension + [example script](examples/README.md) |
| Use Claude, Oh My Pi, or another MCP client | Extension + [MCP adapter](docs/installation.md#run-the-mcp-adapter) |
| Explore Grid sound design with low context switching | [Accessible workflows](docs/accessibility.md) and composition recipes |

## What is supported

- Selected-device, track, container, and project-history inspection.
- Eight exposed remote controls with atomic host-thread writes.
- Device navigation and allowlisted application actions.
- Device insertion by UUID with undo/redo.
- Grid module catalog search, insertion, graph inspection, port connections,
  parameter writes, and native undo when the live capability response exposes
  those operations.
- Semantic Grid modulator search and host-modulator inspection.
- Preview-first shaping sessions with styles, authored profiles, revisions,
  explicit mutation authorization, and session undo.
- Loopback-only local protocol at `127.0.0.1:8765`.

The capability response is authoritative. When `graph_available` is false, the
bridge does not expose graph topology; it must not be inferred from OSC,
coordinates, UI pixels, or native project bytes.

## Quickstart

### Prerequisites

- Bitwig Studio with Controller API 21 or newer.
- Java 21 and Maven.
- Python 3.10 or newer and `uv` for the optional MCP adapter.

### Build and install the extension

```bash
mvn -f extension/pom.xml package
mkdir -p "$HOME/Bitwig Studio/Extensions"
cp extension/target/bitwig-grid-bridge-0.1.0.jar \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
```

Restart Bitwig. Open **Settings → Controllers**, add **Bitwig Grid Bridge**, and
enable it.

### Verify the extension

Open a disposable project from `examples/projects/`, select its Poly Grid, and
run:

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py graph
```

The second command is read-only and prints graph state only when the selected
device exposes it.

### Run the MCP adapter

```bash
uv sync
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run python -m bitwig_mcp_server
```

The adapter uses MCP stdio and keeps stdout reserved for protocol messages. An
MCP client configuration is documented in [Installation](docs/installation.md).

## Safe operating rule

Read capabilities and current state, preview when possible, mutate one thing
with explicit confirmation, then verify. Use a disposable project while
learning. Stop after the first error instead of retrying a mutation blindly.

For detailed procedures:

- [Quickstart](docs/quickstart.md)
- [Installation and troubleshooting](docs/installation.md)
- [Preview-first and graph workflows](docs/workflows.md)
- [Models and capability boundaries](docs/models.md)
- [Tool and recovery cheat sheet](docs/cheatsheet.md)
- [Accessible use](docs/accessibility.md)

## Examples

The [examples](examples/README.md) directory contains two disposable Bitwig
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

See [CONTRIBUTING.md](CONTRIBUTING.md) for scope, safety, and review rules.
