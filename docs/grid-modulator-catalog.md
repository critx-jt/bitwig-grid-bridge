# Grid modulator catalog

The bridge exposes a semantic catalog of modulation-capable Grid packages through
`search_grid_modulators`. The catalog is built from Bitwig's current package
registry at request time; unavailable packages are never advertised or inserted.
The persisted inventory is a reference snapshot, while the bridge response is
authoritative for the selected Bitwig installation.

## Workflow

1. Call `get_grid_capabilities` and confirm `graph_available: true`.
2. Call `search_grid_modulators` with an empty query or a category/name query.
3. Insert a returned `package_id` with `grid_insert_modulator`.
4. Re-read `get_grid_graph` and use its exact `instance_id` values.
5. Tune the inserted module with `grid_set_modulator_parameter`, using the
   native `range` or `options` returned by the live graph.
6. Connect its exact output port to a Grid input with `grid_connect_modulator`.
7. Re-read `get_grid_graph` and verify the connection and parameter values.

Every mutation requires `confirm: true`, unless the active operation is
explicitly cooperative. Insertion does not auto-connect a module: leaving a
new modulator unconnected preserves existing routing.

## Catalog roles

| Category | Use | Representative packages |
| --- | --- | --- |
| `envelope` | Gate- or phase-driven amplitude/control motion | AD, AR, ADSR, Segments |
| `lfo` | Periodic or sample-and-hold motion | LFO, S/H LFO, Wavetable LFO |
| `periodic` | Clocked curve sources | Curves, Slopes |
| `follower` | Audio-derived control signals | Follower, Follower RF |
| `sequencer` | Stepped and register-based motion | Steps, Scale Steps, Step Access, Shift Register |
| `random` | Random or sampled control signals | Chance, Dice, Probabilities, Sample / Hold, Noise |
| `timing` | Clock, gate, and transport synchronization | Clock, Clock Divide, Gate Length, Gate Repeat, Transport |
| `note` | Note, key, velocity, and expression sources | Key On, Note In, Pressure In, Timbre In, Velocity In |
| `external` | Audio, CV, MIDI, hardware, and host inputs | Audio In, Audio Sidechain, CC In, CV In, HW In |
| `utility` | Stable values and modulation range helpers | Constant, Value, Value Scaler |
| `output` | Expose a Grid signal as a Poly Grid modulation source | Modulator Out |

The current live installation returned **50** semantic modulation-capable
packages. This list is intentionally dynamic: package availability and names
come from Bitwig's runtime catalog, while role classification and guidance are
bridge metadata. Use `search_grid_modulators` as the authority rather than
assuming this count remains stable across Bitwig versions.

Parameter writes use Bitwig's native base-value channel, not the transient
modulation/gesture channel. Numeric values may be signed when the live `range`
allows it; integer controls require whole-number option values.

## Tuning patterns

- **LFO:** choose `TIMEBASE`, `WAVE`, `BIPOLAR`, and `RETRIGGER`; use `RATE_IN`
  when another clock should control phase.
- **ADSR / AR / AD:** connect a gate to `GATE_IN`, then use `ATTACK`, `DECAY`,
  `SUSTAIN`, and `RELEASE` from the live parameter metadata.
- **Steps:** set `STEPS`, choose `BIPOLAR`, and use `INTERPOLATION` or
  `DEVICE_PHASE` only when the graph needs those behaviors.
- **Follower:** connect audio to `IN`, then tune attack/decay or response time
  before routing `OUT` into a control input.
- **Modulator Out:** connect a control signal to `IN`; this is a sink and has no
  output port to route onward.

Use native Grid module connections for module-to-module modulation. The
semantic modulator connection command only accepts a source whose package is in
the live modulator catalog; generic `grid_connect_modules` remains available
for other graph topology work.
