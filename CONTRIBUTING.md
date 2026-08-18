# Contributing to Bitwig Grid Bridge

Contributions should improve the Bitwig extension, its local protocol, the
agent-facing adapter, or the disposable Grid examples.

## Development setup

```bash
git clone https://github.com/critx-jt/bitwig-grid-bridge.git
cd bitwig-grid-bridge
uv sync
```

Build the extension with Java 21 and Maven:

```bash
mvn -f extension/pom.xml package
```

## Before opening a pull request

Run the focused checks:

```bash
uv run pytest tests -q
uv run ruff check bitwig_mcp_server tests/test_bridge.py tests/osc/test_controller.py
uv run mkdocs build --strict
mvn -f extension/pom.xml package
```

Live Bitwig tests must use a disposable project under `examples/`. Do not
modify a user's active project or commit generated Bitwig auto-backups.

## Scope and capability claims

The public Bitwig controller API does not expose arbitrary Grid graph
mutation. New code must preserve the explicit `graph_available: false`
boundary unless a supported API is verified. Do not infer module topology from
OSC addresses or undocumented native project bytes.

Mutations must run on Bitwig's host thread, expose a reversible operation where
possible, and return enough state for an agent to verify the result. Add
regression coverage for protocol errors, host-thread scheduling, concurrency,
and project-state boundaries.

Open issues and pull requests at:
https://github.com/critx-jt/bitwig-grid-bridge
