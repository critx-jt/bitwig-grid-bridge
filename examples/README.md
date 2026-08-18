# Grid automation examples

These projects are disposable Bitwig fixtures for the bridge demonstrations.
Copy each project directory into your Bitwig Projects folder or open the
`.bwproject` file directly in Bitwig Studio.

| Project | What it demonstrates |
| --- | --- |
| `projects/polygrid-remote-controls` | Reads a selected Poly Grid and sweeps an exposed remote control atomically. |
| `projects/polygrid-fx-chain` | Selects a Poly Grid and inserts an FX Grid by Bitwig device UUID, with undo support. |

With Bitwig running and **Bitwig Grid Bridge** enabled:

```bash
python examples/automation/grid_bridge_demo.py inspect
python examples/automation/grid_bridge_demo.py sweep --index 2 --duration 4
python examples/automation/grid_bridge_demo.py insert-fx-grid --position after
```

The sweep restores the original value unless `--keep` is supplied. Device
insertion is also reversible by default; pass `--keep` to leave the FX Grid in
the project. Run these commands against the checked-in copies, not a working
music project.

The examples intentionally demonstrate the currently supported surface:
selected-device state, exposed remote controls, container inspection, device
insertion, and undo/redo. They do not claim arbitrary Grid module, port, cable,
or graph mutation because the public Bitwig controller API does not expose that
model.
