# Accessible use

Bitwig Grid Bridge is designed for people who benefit from explicit state,
small steps, low context switching, and reversible actions. This includes AuDHD
and other neurodivergent users, but the practices are useful for anyone working
with a complex audio system.

## Low-load operating pattern

Use one operation at a time:

1. **Name the goal** in one sentence.
2. **Read** the current state.
3. **Choose** one tool.
4. **Preview** when available.
5. **Confirm** the change.
6. **Verify** the result.
7. **Pause** before the next change.

The [workflow page](workflows.md) expands each step. The
[cheat sheet](cheatsheet.md) is intentionally table-heavy for scanning.

## Reduce working-memory load

- Keep a disposable example project open while learning.
- Copy commands from the quickstart instead of reconstructing them.
- Save a parameter snapshot before a multi-step experiment.
- Use names for controls when possible; use indexes only after reading state.
- Keep the MCP session ID and revision together when shaping.
- Stop at the first error. The next read is usually more useful than a retry.

## Make changes predictable

- Preview-first tools do not mutate Bitwig.
- Live mutations require explicit confirmation or an explicitly cooperative
  workflow.
- Successful mutations return a result; verification reads are still required.
- Undo boundaries are named by operation type.
- Stale selected-device state is rejected instead of silently overwritten.
- Graph capability is reported explicitly; unavailable graph data is never
  guessed.

## Sensory and interaction choices

For a shaping brief, state the qualities that matter:

```text
role: sustained background bed
motion: slow and sparse
density: low
contrast: gentle
temperature: cool
surprise: low
```

Start with `hollow` or `glass` for low-intensity exploration. Increase one
control at a time. Leave headroom for performance rather than filling every
control.

## Clear stopping points

A session is complete when all three are true:

- the requested change is visible in the verification response;
- the project is saved or the user intentionally chose not to save;
- the next action is known, or there is a deliberate pause.

It is valid to stop after inspection. It is valid to undo. Neither is failure.

## Documentation features

The site uses:

- short pages with a predictable navigation order;
- headings that describe the decision being made;
- copyable command blocks;
- tables for lookup rather than dense prose;
- light/dark themes with high-contrast accents;
- no information conveyed by color alone;
- direct links to the next likely action.

If a page feels too dense, use the page's headings and follow one code block at
a time. Feedback about reading order, contrast, terminology, or cognitive load
is welcome in a GitHub issue.
