---
name: bitwig-grid-shaping
description: Use for interactive, preview-first Bitwig Grid sound design and device-chain shaping through the Bitwig Grid Bridge MCP server.
---

# Bitwig Grid Shaping

You are shaping an instrument with a human, not batch-editing a file. Make the
composition legible, reversible, and easy to steer.

## Session choreography

1. Ask for or restate the brief in sensory terms: role, motion, density,
   contrast, brightness, warmth, and how much surprise is welcome.
2. Call `get_grid_capabilities` and `get_selected_device_state`.
3. Start one `grid_shape_start` session. Choose a parameter scaffold or a
   `reference` preset as a compositional starting point, not a claim about the
   final sound.
4. Use `grid_shape_compose` for every refinement. Keep controls normalized to
   0-1 and prefer semantic names (`PW`, `Saw %`, `Pitch`) over indexes.
5. Present the returned preview as a concise before → after diff. Ask for
   direction when the brief is ambiguous; do not silently apply.
6. Call `grid_shape_apply` only with the current revision. If the prompt or
   active skill explicitly requests cooperative work that includes the
   mutation, pass `cooperative: true`; otherwise pass `confirm: true`.
7. Call `grid_shape_status` after applying and describe what changed.

## Compositional language

- `glass`: bright, open, precise, lightly animated.
- `ember`: warm, body-forward, restrained movement.
- `acid`: high contrast, narrow pulse width, assertive motion.
- `hollow`: sparse, airy, low-density contour.

These are parameter recipes for exposed controls. They are not substitutes for
listening and do not imply access to the internal Grid graph.

## Authored style profiles

The repository's style profiles encode compositional behavior rather than
internal Grid topology:

- slow, self-running evolution instead of constant activity;
- defined scales and bounded variation instead of unstructured randomness;
- layered drones, noise, oscillators, and diffusion assigned to a clear role;
- density control, because persistent events can become fatiguing quickly;
- deliberate user gestures such as regenerate or performance macros.

Use these authored profiles with `grid_shape_start`:

- `slow-air`: low-intensity glass, slow movement, diffuse space.
- `deep-bed`: low-intensity hollow, sustained drone, sparse background.
- `distant-events`: hollow, rare events, wide space, long tails.
- `soft-drift`: very low intensity, gentle evolution, soft contrast.
- `night-motion`: ember, bounded scale-aware motion, dark atmosphere.
- `layered-motion`: medium intensity, layered diffusion, controlled artifacts.
- `pulse-lab`: higher-intensity acid, bounded variation, reversible regenerate
  gesture.

These profiles are original repository guidance. They do not authorize
downloading, copying, or reconstructing third-party `.bwproject` files.

## Interaction quality bar

- One coherent change per turn; avoid parameter soup.
- Use contrast intentionally: pair a dominant control with one supporting
  control, then leave headroom.
- Preserve the user's current device and parameter state. A stale-state error
  is a cue to re-read, not permission to overwrite.
- Prefer a small number of meaningful revisions over exhaustive sweeps.
- Keep rollback visible: `grid_shape_undo` for a shaping session,
  `grid_project_undo` for insertion or other host operations.

## Viewport layout

When a topology mutation includes placement, keep the graph legible in the
visible Grid viewport:

- use `y=2` for the primary signal lane, `y=7` for a secondary lane, and
  `y=4`/`y=5` for modulation or control sources;
- keep adjacent modules about 3 Grid points apart and align branch endpoints;
- target compact bounds near `x=2..29`, `y=2..7` when the graph fits, leaving
  room for future branches;
- treat `graph-move` as non-persistent in this Bitwig build; persistent
  relayouts require snapshot → clear/reinsert → reconnect → restore parameters
  → save → restart verification.

## Hard boundary

`graph_available: false` is authoritative. Do not fabricate module topology,
ports, cables, coordinates, or `.bwproject` binary patches. For topology-heavy
ideas, use the checked-in disposable projects and report that the public API
cannot express the requested graph mutation.
