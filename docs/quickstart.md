# Quickstart

This page takes a producer from a release asset or clean checkout to a verified
local bridge. Follow the numbered steps in order. Stop at the first failed
check.

## 1. Check prerequisites

You need:

- Bitwig Studio with Controller API 21 or newer.
- The release `.bwextension`, or Java 21 and Maven for a source build.
- Python 3.10 or newer and `uv` for optional MCP use.

The bridge uses loopback only. No cloud account or external network service is
required at runtime.

## 2. Install the extension

Copy the release asset:

```bash
mkdir -p "$HOME/Bitwig Studio/Extensions"
cp BitwigGridBridge.bwextension \
  "$HOME/Bitwig Studio/Extensions/BitwigGridBridge.bwextension"
```

To build from source instead:

```bash
make install-extension
```

Restart Bitwig. Open **Settings → Controllers**, add **Bitwig Grid Bridge**, and
enable it.

## 3. Verify the connection

Open a copy of a project from `examples/projects/`, select its Poly Grid, and
run:

```bash
python examples/automation/grid_bridge_demo.py inspect
```

A healthy response reports the selected device and `ok: true`. If the selected
Grid exposes graph inspection, run the read-only graph check:

```bash
python examples/automation/grid_bridge_demo.py graph
```

If `graph_available` is false, the connection is still usable for exposed
controls. Do not continue with graph operations.

## 4. Make one safe change

For exposed controls, use the preview-first sequence:

```text
get_grid_capabilities → get_selected_device_state
→ grid_shape_start → grid_shape_compose → grid_shape_status
→ grid_shape_apply → grid_shape_status
```

Review the returned before/after values. Applying a draft requires its exact
revision and explicit confirmation. The full sequence is in
[Workflows](workflows.md).

## 5. Add an agent only when needed

The extension and example scripts are sufficient for manual work. For Claude,
Oh My Pi, or another MCP client, follow the
[agent installation reference](agent/index.md).

## If something fails

1. Stop; do not repeat a mutation.
2. Confirm Bitwig is running and the extension is enabled.
3. Run `inspect` again.
4. Confirm the bridge endpoint is free and both programs use `127.0.0.1:8765`.
5. Re-read capabilities before attempting a graph operation.

For recovery steps, see [Cheat sheet](cheatsheet.md).
