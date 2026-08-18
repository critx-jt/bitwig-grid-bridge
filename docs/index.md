# Bitwig Grid Bridge

Bitwig Grid Bridge is a Bitwig Studio controller extension and local
automation protocol for agent-driven Grid workflows.

## What it exposes

- Selected-device and Grid-container inspection
- Eight exposed Bitwig remote controls
- Atomic host-thread parameter batches
- Device insertion by UUID
- Device navigation and project history
- Undo/redo and application actions

The public Bitwig controller API does not expose Grid module graphs, ports,
cables, or coordinates. The bridge reports `graph_available: false` rather than
guessing those structures.

## Start here

- [Installation](installation.md)
- [Architecture](architecture.md)
- Showcase projects: `examples/` in the repository root
