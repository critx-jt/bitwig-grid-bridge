# Engineering and releases

This repository contains two runtime pieces:

- `extension/`: the Java 21 Bitwig controller extension. It owns Bitwig API access and the loopback JSON bridge.
- `bitwig_mcp_server/`: the optional Python MCP adapter. It converts MCP tools into bridge requests and provides shaping and snapshot workflows.

Producer documentation lives in `docs/`. Direct protocol examples live in `examples/automation/`. Agent defaults live in `.omp/`.

## Development prerequisites

- Java 21
- Maven 3.9 or newer
- Python 3.10–3.13
- [`uv`](https://docs.astral.sh/uv/)
- Bitwig Studio with Controller API 21 for live integration checks

Synchronize the pinned Python environment:

```bash
uv sync --frozen
```

Build the extension:

```bash
make build-extension
```

The stable build artifact is:

```text
extension/target/BitwigGridBridge.jar
```

Install it into the current user's Bitwig extensions directory:

```bash
make install-extension
```

Restart Bitwig after replacing the extension file.

## Repository map

| Path | Responsibility |
| --- | --- |
| `extension/src/main/java/` | controller registration, loopback server, Bitwig API access, Grid graph operations |
| `bitwig_mcp_server/bridge/` | newline-delimited JSON client and typed bridge errors |
| `bitwig_mcp_server/osc/` | legacy opt-in compatibility classes; not the supported MCP transport |
| `bitwig_mcp_server/mcp/` | MCP server, tool schemas, execution, shaping sessions, snapshots |
| `examples/automation/` | dependency-free direct bridge demonstrations |
| `tests/` | Python contracts and regression tests |
| `docs/agent/` | agent contracts, safety rules, and tool sequences |
| `.github/workflows/` | CI, documentation deployment, and tagged releases |
| `scripts/build_release_bundle.py` | version validation and ready-to-use bundle assembly |

## Supported architecture

The Java extension is authoritative for live Bitwig state. It binds to `127.0.0.1:8765`, accepts one newline-delimited JSON command at a time, and schedules Bitwig operations on the host thread.

The Python adapter does not inspect project files or reconstruct Grid topology. It reads the bridge and exposes only supported capabilities. Legacy OSC classes remain importable for direct compatibility callers but are disabled by default and are not part of the normal MCP startup path.

Preserve these invariants:

- loopback-only transport;
- serialized request/response framing;
- no Bitwig API work off the host thread;
- mutation authorization before state changes;
- fresh state between dependent mutations;
- native IDs, ranges, options, and indexes from live responses;
- explicit failures rather than inferred or fabricated state;
- a recovery operation where the Bitwig API permits one.

## Change workflow

### Python or MCP change

1. Identify the MCP tool schema and bridge command involved.
2. Preserve the read/preview/mutate boundary.
3. Add or update tests for the observable contract and error path.
4. Update agent documentation when arguments, sequencing, authorization, or recovery changes.
5. Run the focused test while iterating.
6. Run `make test`, `uv run mypy`, and `make check` before review.

### Java bridge change

1. Confirm the operation exists in Controller API 21.
2. Keep all Bitwig API access on the shared host-thread scheduler.
3. Validate request fields before scheduling a mutation.
4. Return enough state for the adapter to verify the outcome.
5. Add Java tests where behavior can be isolated; add Python integration coverage for protocol contracts when practical.
6. Run `make build-extension` and a live Bitwig smoke check.

### New mutation

A new mutation is incomplete without:

- a specific command and JSON schema;
- range, enum, ID, and index validation;
- explicit `confirm` or cooperative authorization at the MCP layer;
- stale-state handling;
- a deterministic error response;
- read-back or returned evidence;
- documented recovery behavior;
- regression coverage for a rejected input and a successful boundary.

Do not add generic write primitives that bypass these contracts.

## Checks

Run the focused Python suite:

```bash
make test
```

Run static checks, a strict documentation build, and the Java package build:

```bash
make check
uv run mypy
```

Build Python wheel and source distribution:

```bash
make build-python
```

Build everything placed in a release:

```bash
make release-bundle
```

The release bundle command validates source versions, builds both language artifacts, copies documentation and examples, and writes:

```text
release/BitwigGridBridge.bwextension
release/bitwig-grid-bridge-VERSION.zip
dist/bitwig_grid_bridge-VERSION-py3-none-any.whl
dist/bitwig_grid_bridge-VERSION.tar.gz
```

Generated `site/`, `dist/`, `release/`, Python caches, and Maven `target/` trees are ignored. Do not commit them.

## Live Bitwig smoke check

Unit tests cannot prove Bitwig registration or host-thread behavior. Before a release:

1. Run `make install-extension`.
2. Restart Bitwig.
3. Enable **Bitwig Grid Bridge** in **Settings → Controllers**.
4. Open a disposable project under `examples/projects/`.
5. Run:

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py graph
```

6. Start the optional adapter:

```bash
BITWIG_MCP_GRID_BRIDGE_ENABLED=true uv run bitwig-mcp
```

7. Call `get_grid_capabilities` and `get_selected_device_state` from an MCP client.
8. Perform one preview-only shaping call.
9. If testing mutation, use a disposable project, make one confirmed change, verify read-back, and exercise the matching undo.
10. Stop the adapter and confirm the bridge still serves a direct read request.

Do not run live mutation tests against a user's working project.

## CI behavior

`Bridge CI` runs on pushes and pull requests to `main`:

- Python tests on Python 3.10, 3.11, 3.12, and 3.13;
- Ruff, mypy, strict MkDocs, and Maven packaging;
- Python wheel and source-distribution builds;
- Java extension artifact upload.

The reusable setup action pins `uv` and synchronizes `uv.lock` with `--frozen`. Update the action pin and regenerate the lock in the same change when required.

`Documentation` builds MkDocs with `--strict` and deploys only from `main` when documentation inputs change.

## Release procedure

Releases are tag-driven. The tag, Python project, Maven project, and extension definition must use the same semantic version.

### Prepare

1. Choose `X.Y.Z`.
2. Update:
   - `pyproject.toml` → `[project].version`
   - `extension/pom.xml` → project `<version>`
   - `GridBridgeExtensionDefinition.getVersion()`
3. Run `uv lock` if dependency metadata changed.
4. Run:

```bash
make test
uv run mypy
make check
make release-bundle
```

5. Inspect the release bundle and install its `BitwigGridBridge.bwextension` in Bitwig for the live smoke check.
6. Commit the version and release changes.

### Publish

Create and push an annotated version tag:

```bash
git tag -a vX.Y.Z -m "Bitwig Grid Bridge X.Y.Z"
git push origin main vX.Y.Z
```

The release job:

1. waits for all CI jobs;
2. checks that `vX.Y.Z` matches the Python package version;
3. validates all three source versions during bundle assembly;
4. rebuilds the extension, wheel, source distribution, and bundle;
5. creates a GitHub release with generated notes;
6. attaches the ready-to-install `.bwextension`, full bundle, wheel, and source distribution.

A version mismatch fails before publication. Do not retag a different commit. Correct the source versions and create a new version tag.

## Release bundle contents

The ZIP is intended for both producers and technical integrators. It contains:

- `BitwigGridBridge.bwextension`, ready to copy into Bitwig's Extensions directory;
- the Python package source and locked environment;
- wheel and source distribution under `python/`;
- producer, agent, protocol, scripting, and engineering documentation;
- direct automation examples and sample Bitwig projects;
- Java extension source for optional Maven rebuilding;
- the `.omp` MCP client template and agent skill;
- `INSTALL.txt` with the shortest setup path.

Maven is optional for users installing the bundled extension. It is required only to build or modify the Java extension.

## Dependency maintenance

Runtime and development dependencies are exact-pinned in `pyproject.toml`; transitive versions are frozen in `uv.lock`.

For a dependency update:

1. inspect release notes and supported Python versions;
2. change the direct pin;
3. run `uv lock`;
4. run `uv tree --outdated` to review remaining drift;
5. audit both runtime-only and complete locked exports;
6. run all checks and build both artifacts;
7. inspect `uv.lock` for unintended major changes.

Do not add a test, lint, build, or release dependency merely because a removed workflow used it. Keep each tool tied to a current command in `Makefile` or CI.

## Review checklist

- No generated build or documentation output is tracked.
- Tool schemas and executor branches agree.
- Exported behavior has regression coverage.
- Mutation gates and stale-state behavior remain explicit.
- Producer and agent docs describe the same supported transport.
- Direct scripts stop on ambiguous errors.
- Python and Java source versions agree for releases.
- `make test`, `uv run mypy`, `make check`, and `make release-bundle` pass.
- A disposable-project Bitwig smoke check covers registration, read state, and recovery.
