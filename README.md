# Bitwig Grid Bridge

Bitwig Grid Bridge is a local Bitwig Studio controller extension for inspecting devices, shaping exposed controls, and editing supported Grid graphs. An optional Python adapter exposes the bridge as Model Context Protocol tools for agents.

[Producer documentation](https://critx-jt.github.io/bitwig-grid-bridge/) · [Installation](docs/installation.md) · [Workflows](docs/workflows.md) · [Agent playbook](docs/agent/workflows.md) · [Engineering](docs/engineering.md)

## What is included

- A Java 21 Bitwig controller extension using Controller API 21.
- A loopback-only newline-delimited JSON bridge at `127.0.0.1:8765`.
- Direct automation examples that work without MCP.
- An optional stdio MCP adapter with inspect, catalog, shaping, graph-edit, navigation, snapshot, and recovery tools.
- Producer, scripting, agent, protocol, and engineering documentation.
- Tag-driven release automation for a ready-to-install `.bwextension`, full bundle, Python wheel, and source distribution.

The Java extension is authoritative for Bitwig state. The Python adapter does not parse projects or infer missing Grid topology.

## Install a release

Download `BitwigGridBridge.bwextension` from the latest GitHub release and copy it into the current user's Bitwig Extensions directory:

```bash
mkdir -p "$HOME/Bitwig Studio/Extensions"
cp BitwigGridBridge.bwextension "$HOME/Bitwig Studio/Extensions/"
```

Restart Bitwig, open **Settings → Controllers**, add **Bitwig Grid Bridge**, and enable it.

The `bitwig-grid-bridge-VERSION.zip` release asset also contains the Python adapter, locked environment, documentation, examples, source, and Python distributions. See [Installation](docs/installation.md).

## Verify without MCP

Open a project, select a device, and run:

```bash
python examples/automation/grid_bridge_demo.py inspect
```

For a supported selected Grid:

```bash
python examples/automation/grid_bridge_demo.py graph
```

The included script also demonstrates bounded parameter sweeps and reversible device insertion. See [Automation scripts](docs/scripting.md).

## Use the optional MCP adapter

From a source checkout or full release bundle:

```bash
uv sync --frozen
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run bitwig-mcp
```

A client configuration template is available at [`.omp/mcp.json`](.omp/mcp.json). The supported MCP path requires the local Grid Bridge; it does not fall back to OSC.

Use [Producer workflows](docs/workflows.md) for musical procedures. MCP integrators should use the [Agent workflow playbook](docs/agent/workflows.md), [tool reference](docs/agent/tools.md), and [data and safety rules](docs/agent/models.md).

## Build from source

Requirements: Java 21, Maven, Python 3.10–3.13, and `uv`.

```bash
uv sync --frozen
make build-extension
make test
make check
uv run mypy
```

Install the source-built extension:

```bash
make install-extension
```

Build Python distributions and the complete local release bundle:

```bash
make build-python
make release-bundle
```

`make check` runs Ruff, a strict MkDocs build, and the Maven package build. Live Bitwig integration checks use a disposable project and are documented separately in [Engineering and releases](docs/engineering.md).

## Safety model

- Observe current capabilities and selection before every operation.
- Treat `graph_available: false` as a hard graph boundary.
- Use package IDs from live catalogs and instance IDs, ports, coordinates, ranges, and options from the latest graph.
- Preview shaping before applying an exact revision.
- Require explicit confirmation for mutations unless the prompt is explicitly cooperative.
- Re-read state after every dependent mutation.
- Never automatically retry an ambiguous mutation timeout.
- Keep an undo, snapshot, or project recovery path.

## Repository layout

```text
extension/               Java Bitwig extension
bitwig_mcp_server/       Optional Python MCP adapter
examples/automation/     Direct protocol scripts
examples/projects/       Disposable Bitwig projects
docs/                    Producer, agent, scripting, and engineering guides
.omp/                    Oh My Pi MCP and agent configuration
scripts/                 Release bundle assembly
```

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [Engineering and releases](docs/engineering.md). Changes to mutation behavior must include validation, recovery semantics, regression coverage, and matching producer/agent documentation.

## License

MIT. See [LICENSE](LICENSE).
