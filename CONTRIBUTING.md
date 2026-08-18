# Contributing to Bitwig Grid Bridge

Contributions should improve the Bitwig extension, local bridge protocol, optional MCP adapter, documentation, or disposable examples. Read [Engineering and releases](docs/engineering.md) before changing runtime or release behavior.

## Development setup

```bash
git clone https://github.com/critx-jt/bitwig-grid-bridge.git
cd bitwig-grid-bridge
uv sync --frozen
make build-extension
```

Java changes require Java 21 and Maven. Python supports versions 3.10–3.13.

## Before opening a pull request

```bash
make test
uv run mypy
make check
make build-python
```

For changes to release assembly, also run:

```bash
make release-bundle
```

Live Bitwig tests must use a disposable project under `examples/projects/`. Do not modify a user's active project or commit generated Bitwig auto-backups.

## Runtime contracts

The Java extension is authoritative for Bitwig state. Keep bridge traffic loopback-only and serialize Bitwig API work through the host-thread scheduler.

New mutations must provide:

- validated arguments, IDs, indexes, ranges, and options;
- explicit confirmation or cooperative authorization;
- stale-state rejection;
- deterministic failure responses;
- read-back evidence;
- a documented recovery path where the Bitwig API permits one;
- regression coverage for successful and rejected boundaries.

The public Bitwig controller API does not expose arbitrary Grid graph mutation on every selected device. Preserve `graph_available: false` unless a supported capability is verified. Do not infer topology from OSC addresses, interface state, stale snapshots, or undocumented project bytes.

## Documentation

Update both audiences when behavior changes:

- producer procedures in `docs/workflows.md` or `docs/scripting.md`;
- agent sequencing and safety in `docs/agent/`;
- installation, build, and release instructions in `docs/installation.md` and `docs/engineering.md`.

Run the strict MkDocs build through `make check`. Broken navigation, links, and undocumented tool contracts are release blockers.

Open issues and pull requests at <https://github.com/critx-jt/bitwig-grid-bridge>.
