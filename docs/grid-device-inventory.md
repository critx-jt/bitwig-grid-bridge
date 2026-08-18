# Live Grid device inventory

Snapshot revision **3** (sha256-fcb97ba6e2ec30de66c2366f48c7bb26d6379dd93ed1ce828d69be287bb04aa2) captured from Bitwig Studio **6.0.11** on **2026-08-18T14:57:29.953Z**. This is a reference snapshot, not a substitute for a live capability and graph read.

## Authority and scope

- `docs/grid-device-inventory.json` is the machine-readable inventory, including every installed package, every captured graph instance, and per-parameter native ranges/options.
- The bridge is authoritative at session time. Start with `get_grid_capabilities`, then read `get_grid_graph` when graph access is available.
- Catalog package IDs are insertion identifiers. Instance IDs and coordinates belong only to the captured `polygrid_example` project and must be re-read before mutation.
- If the bridge reports `graph_available: false`, do not infer modules, ports, cables, coordinates, or parameter metadata from UI state, stale snapshots, or project-file bytes.

## Provenance and revision

| Field | Value |
| --- | --- |
| Inventory revision | 3 |
| Revision ID | `sha256-fcb97ba6e2ec30de66c2366f48c7bb26d6379dd93ed1ce828d69be287bb04aa2` |
| Bitwig version | **6.0.11** |
| Version source | Bitwig project app-version and ~/.BitwigStudio/latest-launched-version.txt |
| Project | `polygrid_example` |
| Captured at | 2026-08-18T14:57:29.953Z |
| Project modified at capture | false |
| Bridge protocol | 3 |
| Graph class | `com.bitwig.flt.document.core.master.device.vT1` |

The revision ID is a SHA-256 digest of the inventory payload with `revision_id` set to `null`. Re-capture after a Bitwig upgrade, package change, project change, or bridge protocol change.

## Coverage summary

| Field | Count |
| --- | ---: |
| Installed catalog packages | 232 |
| Graph module instances | 235 |
| Devices with a captured instance | 232 |
| Captured parameters | 903 |
| Numeric parameters with native ranges | 479 |
| Numeric parameters without native ranges | 119 |
| Boolean parameters with options | 305 |
| Discrete parameters with options | 105 |
| Catalog packages missing from graph | 0 |

All 232 catalog packages have one or more graph instances. The graph contains 3 additional instances because the starting project already contained duplicate instances of existing packages. No new modules were connected; the pre-existing Union → ADSR → Audio Out routing was preserved.

## Bridge capability snapshot

| Field | Value |
| --- | --- |
| Protocol | 3 |
| Graph class | `com.bitwig.flt.document.core.master.device.vT1` |
| graph_available | true |
| graph_inspection | true |
| module_catalog | true |
| module_insertion | true |
| port_connections | true |
| native_undo | true |

## Parameter metadata

Each row below is taken from a live graph instance. Parameter fields are preserved exactly in the JSON snapshot:

- `value`: current bridge-reported native base value. Float and integer values use Bitwig parameter units, not normalized fractions.
- `range`: native Bitwig parameter range from the runtime parameter definition; use it to validate writes.
- `options`: boolean choices or discrete option values and labels exposed by Bitwig. Numeric options are the values accepted by the discrete control.
- `display`: current human-readable Bitwig display string.
- `metadata unavailable`: the runtime exposed a writable-looking stream entry without a safe current value, native range, or option list; do not infer a value or range.

## Captured graph instances

The captured graph contains **235 modules**. Existing routing remains explicit in each input connection. Coordinates are intentionally spread across free cells so every catalog package is present without introducing new cables.

| Instance | Module | Package ID | Coordinates | Inputs | Outputs |
| --- | --- | --- | --- | --- | --- |
| 0 | **Union** | `df0a08cc-68b4-4fb2-a662-05cb09745e37` | (-2, -1) | PITCH_IN<br>PHASE_IN<br>GATE_IN | OUT (0) |
| 1 | **ADSR** | `7e09068b-fee5-457e-afe4-7017661ebbd3` | (1, -1) | GATE_IN<br>IN ← 0:OUT | MOD_OUT (0)<br>OUT (1)<br>BIASED_OUT (2) |
| 2 | **Audio Out** | `af7b5503-c955-489e-9461-164107d56bb6` | (4, -1) | IN ← 1:OUT | — |
| 3 | **AD** | `5b7ab937-4f09-41fc-a379-983fb597b2ff` | (-30, -30) | GATE_IN<br>IN | MOD_OUT (0)<br>OUT (1) |
| 4 | **ADSR** | `7e09068b-fee5-457e-afe4-7017661ebbd3` | (-26, -30) | GATE_IN<br>IN | MOD_OUT (0)<br>OUT (1)<br>BIASED_OUT (2) |
| 5 | **AM/RM** | `e1d4fdf5-057e-4c83-869e-db4ee322e4ce` | (-22, -30) | IN<br>IN2 | OUT (0) |
| 6 | **AND** | `1e330c79-9a6f-4015-8dfa-da507c1bb15a` | (-18, -30) | IN<br>IN2 | OUT (0) |
| 7 | **AR** | `9eaf8e7d-b8f7-4134-85c1-c7c77dd9fe92` | (-14, -30) | GATE_IN<br>IN | MOD_OUT (0)<br>OUT (1) |
| 8 | **Abs** | `895470df-c2de-417f-9113-8bb6fe948b6d` | (-10, -30) | IN | OUT (0)<br>SIGN (1) |
| 9 | **Accents** | `a0b3bd86-a4a9-4eac-83fc-468840332778` | (-6, -30) | PHASE_IN | OUT (0)<br>OUT2 (1) |
| 10 | **Add** | `57a6f72c-db9d-4a96-bc4b-d6a2bb8b656a` | (-2, -30) | IN<br>IN2 | OUT (0) |
| 11 | **All-pass Delay** | `f435652c-2fd7-4edd-8b7a-ee97b0fd43a5` | (2, -30) | IN | OUT (0) |
| 12 | **All-pass** | `b1682757-4fcf-4b5f-bfe7-58dd81d79954` | (6, -30) | IN | OUT (0) |
| 13 | **Amplify** | `a6cd650b-c4de-46c6-8741-c07a0a9bfec2` | (10, -30) | IN | OUT (0) |
| 14 | **Array** | `010ba490-caf6-4af6-93bd-82d9be63610c` | (14, -30) | READ_POS<br>IN<br>WRITE_POS<br>GATE_IN | OUT (0) |
| 15 | **Attenuate** | `cfc56753-defc-4324-8a68-bf747ff45508` | (18, -30) | IN | OUT (0) |
| 16 | **Audio In** | `b2a6b111-7afd-4c95-b380-6de8125af980` | (22, -30) | — | OUT (0) |
| 17 | **Audio Out** | `af7b5503-c955-489e-9461-164107d56bb6` | (26, -30) | IN | — |
| 18 | **Audio Sidechain** | `59a10d46-c6a2-4676-a0fb-8a2923636d82` | (30, -30) | — | OUT (0) |
| 19 | **Average** | `2cbbf968-2a51-48ab-9e1f-ba665a52ea8b` | (-30, -26) | IN | OUT (0) |
| 20 | **Bend** | `c7d55e0b-33c6-4436-ba37-d1f1a0953893` | (-26, -26) | IN | OUT (0) |
| 21 | **Bi → Uni** | `97f5eff7-7619-4957-aa8f-5cfc353d56d6` | (-22, -26) | IN | OUT (0) |
| 22 | **Bias** | `c5aee529-9dce-406d-87cd-0f1cabcac13f` | (-18, -26) | IN | OUT (0) |
| 23 | **Bite** | `18b292a7-c11c-4014-b563-0784601e7cc8` | (-14, -26) | PITCH_IN<br>PHASE_IN<br>GATE_IN | OUT (0) |
| 24 | **Blend** | `0f2a027d-2bc3-4789-8a56-4d079a7e6137` | (-10, -26) | IN<br>IN2 | OUT (0) |
| 25 | **Button** | `c0281e6e-3d55-4e86-8c9b-0ce8cf3db67d` | (-6, -26) | — | OUT (0) |
| 26 | **CC In** | `311f3697-7323-46a0-a00b-1c51b12042e9` | (-2, -26) | — | OUT (0) |
| 27 | **CC Out** | `131d870c-0df7-4f28-a536-cd13e82af404` | (2, -26) | IN | — |
| 28 | **CV In** | `632c2ab7-5c5a-493a-af69-ba4ada9997eb` | (6, -26) | — | OUT (0) |
| 29 | **CV Out** | `f137c16d-d9a3-471d-9e1d-586722988695` | (10, -26) | IN | — |
| 30 | **CV Pitch In** | `cc87d3c3-46f5-41e3-91d9-882243cdf717` | (14, -26) | — | OUT (0) |
| 31 | **CV Pitch Out** | `502771b2-1a4f-44c4-9038-03cac7da59e7` | (18, -26) | IN | — |
| 32 | **Ceil** | `321563fe-42e4-4353-84e2-bd95db6a00e4` | (22, -26) | IN | OUT (0)<br>REMAINDER (1) |
| 33 | **Chance** | `fe6be8de-5abf-4825-99d7-c2127f039bb4` | (26, -26) | IN<br>MOD_IN | OUT (0) |
| 34 | **Chebyshev** | `0b9d73b3-796f-4cc0-b7af-d59e19df2827` | (30, -26) | IN | OUT (0) |
| 35 | **Chorus+** | `537b38d0-8ad3-4fa0-aa24-82c7c56c3d21` | (-30, -22) | IN | OUT (0) |
| 36 | **Clip** | `d9309744-b38c-4f40-95de-ee56bb073f4e` | (-26, -22) | IN | OUT (0) |
| 37 | **Clock Divide** | `a072e864-32de-4c4c-a334-2ed9afab0965` | (-22, -22) | RESET_IN<br>IN | OUT (0) |
| 38 | **Clock Quantize** | `86d811e8-e1df-470b-9740-3bf3d924d87a` | (-18, -22) | IN<br>GATE_IN | OUT (0) |
| 39 | **Clock** | `245af7f8-1137-4b44-abc3-b5e1f52fe016` | (-14, -22) | GATE_IN | GATE_OUT (0)<br>OUT (1) |
| 40 | **Comb** | `b84241c5-b8b7-403f-8422-8195cf6d3478` | (-10, -22) | IN<br>MOD_IN | OUT (0) |
| 41 | **Comment** | `b297dabd-144e-4106-b8da-15d08fa6b124` | (-6, -22) | — | — |
| 42 | **Constant** | `5412a6f2-9920-41b5-af13-ea64d266a26d` | (-2, -22) | — | OUT (0) |
| 43 | **Crossover-2** | `6ecd5ea8-9105-4350-af41-b2870ca54364` | (2, -22) | IN | OUT (0)<br>OUT2 (1) |
| 44 | **Crossover-3** | `979bec96-fea9-4d7d-9657-65a447709b50` | (6, -22) | IN | OUT3 (0)<br>OUT2 (1)<br>OUT (2) |
| 45 | **Curve** | `1093d01f-f6ba-4eef-8a62-3409d4d365ab` | (10, -22) | IN | OUT (0) |
| 46 | **Curves** | `2302d0d8-afc0-4ed6-86ef-6d1dffeda6a2` | (14, -22) | RATE_IN<br>GATE_IN<br>PHASE_IN | OUT (0) |
| 47 | **Delay** | `e2e808c8-6b7e-4a00-9563-39e2f44177da` | (18, -22) | IN | OUT (0) |
| 48 | **Dice** | `9f66c3b9-ca9b-4b62-8792-73fbec6464a4` | (22, -22) | IN | OUT (0) |
| 49 | **Diode** | `8399cc4f-57a6-48aa-a38b-2dac60fd15f8` | (26, -22) | IN | OUT (0) |
| 50 | **Distortion** | `6e8f9374-3393-4531-9f7e-571d0033ea94` | (30, -22) | IN | OUT (0) |
| 51 | **Divide** | `21a1b455-fa76-4662-ad31-e89fbe0fcd65` | (-30, -18) | IN<br>IN2 | OUT (0) |
| 52 | **Dome** | `fa194943-ad9a-4106-9aa9-9e2df5e44593` | (-26, -18) | IN | OUT (0)<br>OUT2 (1)<br>OUT3 (2)<br>OUT4 (3) |
| 53 | **=** | `e4fda749-9129-4f03-ba7a-06099575ced6` | (-22, -18) | IN<br>IN2 | OUT (0) |
| 54 | **Exp** | `eca1e042-b7ac-4f9e-863d-e5f32f6755da` | (-18, -18) | IN | OUT (0) |
| 55 | **Exponents** | `0ef176bd-a46a-424f-a163-2fc2276a9779` | (-14, -18) | IN | OUT (0) |
| 56 | **Fizz** | `d9e01995-14fc-4bae-a727-0fe2aa40c338` | (-10, -18) | IN<br>MOD_IN | OUT (0) |
| 57 | **Flanger+** | `00b09256-db30-40d5-b94f-c22477e49b5c` | (-6, -18) | IN<br>MOD_IN | OUT (0) |
| 58 | **Floor** | `b0f4c3b2-eae2-44b3-805b-9d8d4c45ee34` | (-2, -18) | IN | OUT (0)<br>REMAINDER (1) |
| 59 | **Follower RF** | `0a1490cc-7df2-470c-b48e-6889b0f0361b` | (2, -18) | IN | OUT (0) |
| 60 | **Follower** | `165fd92f-ed5e-4a54-97ed-99f334e28801` | (6, -18) | IN | OUT (0) |
| 61 | **Freq Shift+** | `904717d9-f24e-4742-9c75-b61ca0bf97bd` | (10, -18) | RATE_IN<br>PHASE_IN<br>IN | OUT (0) |
| 62 | **Freq → Pitch** | `fc1fba88-7413-41a4-9427-7251a44ac040` | (14, -18) | IN | OUT (0) |
| 63 | **Gain - Vol** | `b1296326-cbf0-4797-9fc6-e2a6f2ce4a78` | (18, -18) | IN | OUT (0) |
| 64 | **Gain - dB** | `b2c6ef93-8a14-4e10-b152-56bcee883e1c` | (22, -18) | IN | OUT (0) |
| 65 | **Gain In** | `e470fc3b-4979-4c3b-aa79-27e6c49a3b88` | (26, -18) | — | OUT (0) |
| 66 | **Gate In** | `4e00fda6-20f6-45a9-9d7e-02867cf09b82` | (30, -18) | — | OUT (0) |
| 67 | **Gate Length** | `7b001029-62eb-4c40-81ab-13828622f3fd` | (-30, -14) | IN | OUT (0) |
| 68 | **Gate Repeat** | `71508287-dc35-4e62-b1a0-82ba2a2d8ef7` | (-26, -14) | IN | OUT (0) |
| 69 | **Gates** | `8d644ad7-8d77-4f05-a36e-04a57f719635` | (-22, -14) | PHASE_IN | OUT (0) |
| 70 | **≥** | `d6008d9a-57b1-416a-ae5c-795dd386c674` | (-18, -14) | IN<br>IN2 | OUT (0) |
| 71 | **>** | `7b681143-c276-49b9-9fed-1ce51d33aa39` | (-14, -14) | IN<br>IN2 | OUT (0) |
| 72 | **HW In** | `d8195834-0238-4a18-bcba-d79efafa6f25` | (-10, -14) | — | OUT (0) |
| 73 | **HW Out** | `49f0844b-e202-4011-b0a4-0d9f7c2ff41e` | (-6, -14) | IN | — |
| 74 | **Hard Clip** | `5ae67be0-65a0-4905-84b4-1908baaf5613` | (-2, -14) | IN | OUT (0) |
| 75 | **Heat** | `cc13faed-d9c5-47b5-aca6-d0adbe0afdb5` | (2, -14) | IN | OUT (0) |
| 76 | **High-pass** | `052cbe38-8ace-4ded-a4a9-de80a9f5fcea` | (6, -14) | IN | OUT (0) |
| 77 | **Hold** | `9671cb0e-7272-4d50-9d2e-a207971983cf` | (10, -14) | IN<br>GATE_IN | OUT (0) |
| 78 | **Howl** | `5d528874-cf9f-48e8-9386-b3118a38d279` | (14, -14) | IN | OUT (0) |
| 79 | **Invert** | `378e9b7d-0b95-4032-a12a-36d345550fab` | (18, -14) | IN | OUT (0) |
| 80 | **Key On** | `6ba4eb9c-3ac6-4246-a4bd-192d395a3a58` | (22, -14) | — | OUT (0) |
| 81 | **Keys Held** | `ea6c6b9d-831b-4c05-a26b-2b1dadf81e0e` | (26, -14) | — | OUT (0) |
| 82 | **LFO** | `b89c1bce-203a-46be-8869-a44eb7868860` | (30, -14) | RATE_IN<br>GATE_IN<br>PHASE_IN | OUT (0) |
| 83 | **LR Gain** | `6a9e4b04-0e24-424f-abe3-a23b0744319a` | (-30, -10) | IN | OUT (0) |
| 84 | **Label** | `b3a19e19-da13-491d-b569-16ff5cbb109b` | (-26, -10) | — | — |
| 85 | **Lag** | `a4d23895-2761-476b-9aad-cbe372d286ea` | (-22, -10) | IN | OUT (0) |
| 86 | **Latch** | `61810948-1f33-4bc5-a8bb-d30c78e0afde` | (-18, -10) | IN<br>SET_IN<br>RESET_IN | OUT (0) |
| 87 | **≤** | `a5080bc6-2ee1-4a97-ad52-511f2a88343f` | (-14, -10) | IN<br>IN2 | OUT (0) |
| 88 | **<** | `c28a54ec-c679-4d09-b086-aa10fbae3b95` | (-10, -10) | IN<br>IN2 | OUT (0) |
| 89 | **Level Scaler** | `800377c2-1f1c-4804-9440-4c6531047818` | (-6, -10) | IN | OUT (0) |
| 90 | **Level** | `0565644e-7e9f-45bf-bc34-8df52b5d7d80` | (-2, -10) | — | OUT (0) |
| 91 | **Lin → dB** | `7091f45b-eb29-41e9-a285-c6173cf52288` | (2, -10) | IN | OUT (0) |
| 92 | **Log** | `1c5671ab-6e13-4b60-90fd-b64142d4004d` | (6, -10) | IN | OUT (0) |
| 93 | **Logic Delay** | `ec697982-2be4-4b87-88d4-333032f18577` | (10, -10) | IN | OUT (0) |
| 94 | **Long Delay** | `f601a44c-8dcb-4ee7-9f2a-ce02ff07948e` | (14, -10) | IN | OUT (0) |
| 95 | **Low-pass LD** | `85ca7753-049a-419a-bb37-d8c358b10932` | (18, -10) | IN<br>MOD_IN | OUT (0) |
| 96 | **Low-pass MG** | `a72eb152-884e-4bf0-bd22-d21e49fd3466` | (22, -10) | IN<br>MOD_IN | OUT (0) |
| 97 | **Low-pass** | `9747205f-2450-42da-89be-200b149b967b` | (26, -10) | IN | OUT (0) |
| 98 | **Merge** | `c10b5ffa-0d10-4005-ad49-a39253ee26eb` | (30, -10) | MOD_IN<br>IN<br>IN2<br>IN3<br>IN4<br>IN5<br>IN6<br>IN7<br>IN8 | OUT (0) |
| 99 | **MinMax** | `aaf43587-9228-4bb0-8743-8cbf411e6be7` | (-30, -6) | IN<br>IN2 | OUT (0)<br>OUT2 (1) |
| 100 | **Mixer** | `839e96da-cda4-45ce-b5a1-e0a40a176968` | (-26, -6) | IN<br>IN2<br>IN3<br>IN4<br>IN5<br>IN6 | OUT (0) |
| 101 | **Mod Delay** | `a8d565fa-fcf5-4ede-bea9-90999f6e8406` | (-22, -6) | IN<br>MOD_IN | OUT (0) |
| 102 | **Modulator Out** | `098ad9c6-b4c9-4ec1-887f-eaf588611056` | (-18, -6) | IN | — |
| 103 | **Multiply** | `4a945068-35ff-469f-bc17-fda5d32b7baa` | (-14, -6) | IN<br>IN2 | OUT (0) |
| 104 | **N-Latch** | `04685f05-a0bd-4cef-81f8-b59a2e2e16d1` | (-10, -6) | IN<br>IN2<br>IN3<br>IN4<br>IN5<br>IN6<br>IN7<br>IN8 | OUT (0)<br>OUT2 (1)<br>OUT3 (2)<br>OUT4 (3)<br>OUT7 (4)<br>OUT8 (5)<br>OUT6 (6)<br>OUT5 (7) |
| 105 | **NAND** | `328047a0-d0ff-47c6-93ac-44236e228157` | (-6, -6) | IN<br>IN2 | OUT (0) |
| 106 | **NOR** | `5b278498-4ba5-415b-b159-337edebf952d` | (-2, -6) | IN<br>IN2 | OUT (0) |
| 107 | **NOT** | `71d887c3-77b6-4ebd-86a9-a23f54a0d606` | (2, -6) | IN | OUT (0) |
| 108 | **Noise** | `33344afa-c8fb-450f-8e82-65fd242a7837` | (6, -6) | — | OUT (0) |
| 109 | **≠** | `96507541-21a4-45a0-8bc6-48874e7de89e` | (10, -6) | IN<br>IN2 | OUT (0) |
| 110 | **Note In** | `06c1eac9-4d64-4748-8d52-8bf18324d1e7` | (14, -6) | — | GATE_OUT (0)<br>PITCH_OUT (1)<br>VELOCITY_OUT (2)<br>TIMBRE_OUT (3)<br>PRESSURE_OUT (4)<br>GAIN_OUT (5)<br>PAN_OUT (6)<br>CHANNEL_OUT (7) |
| 111 | **Note Out** | `70baf51d-271c-43c3-b2de-c98fc48f326d` | (18, -6) | GATE_IN<br>PITCH_IN<br>VELOCITY_IN<br>CHANNEL_IN<br>TIMBRE_IN<br>PRESSURE_IN<br>GAIN_IN<br>PAN_IN | — |
| 112 | **OR** | `3d31b4e4-ce56-4992-a793-39b362f8003a` | (22, -6) | IN<br>IN2 | OUT (0) |
| 113 | **Octaver** | `85c173a2-1eb3-4cc1-a19d-84bcb4bde00b` | (26, -6) | IN | OUT (0) |
| 114 | **Oscilloscope** | `0a3b591d-a9b5-44dd-a6ee-a00794df4dc5` | (30, -6) | IN<br>IN2<br>GATE_IN | OUT (0)<br>OUT2 (1) |
| 115 | **Pan In** | `3f482022-4a2c-4484-a5d8-d93a1d74e105` | (-30, -2) | — | OUT (0) |
| 116 | **Pan** | `43600afd-7226-4408-bbb6-b7b9cc2a6cee` | (-26, -2) | IN | OUT (0) |
| 117 | **Ø Bend** | `c2d6358d-9053-49a3-9e1d-9b6c8d0bd539` | (-22, -2) | IN | OUT (0) |
| 118 | **Ø Counter** | `f9b5157c-0a41-403c-810b-9bbf9a133110` | (-18, -2) | RESET_IN<br>GATE_IN | OUT (0) |
| 119 | **Ø Formant** | `9cab8245-ebbf-42ec-ba95-e7bcca4a9cab` | (-14, -2) | IN | OUT (0) |
| 120 | **Phase In** | `94d89ce0-4a98-4b95-be4a-36814d7b1855` | (-10, -2) | — | OUT (0) |
| 121 | **Ø Lag** | `c03fc75f-c65b-452c-96ea-2ff8de806c26` | (-6, -2) | IN | OUT (0) |
| 122 | **Ø Mirror** | `de0334b8-93bd-463e-824b-dea397e90354` | (-2, -2) | IN | OUT (0) |
| 123 | **Ø Pinch** | `32323ba6-3a23-4c2d-a2c8-439961ba66ae` | (2, -2) | IN | OUT (0) |
| 124 | **Ø Pulse** | `ecab3feb-20ad-494c-9a18-17536832002e` | (6, -2) | IN | OUT (0) |
| 125 | **Ø Reset** | `d04bb748-5f66-4a4a-85d8-d3402c982e22` | (10, -2) | GATE_IN<br>IN | OUT (0) |
| 126 | **Ø Reverse** | `89f9e7d1-e36c-446f-937e-a881bf90c7c9` | (14, -2) | IN | OUT (0) |
| 127 | **Ø Saw** | `4d7201c8-304a-4b42-95a2-5cc2fa945c18` | (18, -2) | IN | OUT (0) |
| 128 | **Ø Scaler** | `53de290f-e7e0-4c71-95d4-dad2c8652691` | (22, -2) | GATE_IN<br>IN | GATE_OUT (0)<br>OUT (1) |
| 129 | **Ø Shift** | `727cf275-dd41-4c5a-865d-efee322c04a7` | (26, -2) | IN | OUT (0) |
| 130 | **Ø Sine** | `2d356600-6e66-49a2-91e5-c14397956a7a` | (30, -2) | IN | OUT (0) |
| 131 | **Ø Sinemod** | `1c248b5d-47ef-401c-94c3-1f4f24d6a88a` | (-30, 2) | IN | OUT (0) |
| 132 | **Ø Skew** | `4f2ab665-8fca-4a03-b3b5-f85acdcf393a` | (-26, 2) | IN | OUT (0) |
| 133 | **Ø Split** | `f7272bf8-b86a-491c-b342-8eae1a792da4` | (-22, 2) | IN | OUT (0)<br>OUT1 (1)<br>OUT2 (2)<br>OUT3 (3)<br>OUT4 (4)<br>OUT5 (5)<br>OUT6 (6)<br>OUT7 (7) |
| 134 | **Ø Sync** | `1cd61fc6-74a8-4117-bdb3-54bc8b033f8a` | (-18, 2) | IN | OUT (0) |
| 135 | **Ø Triangle** | `af9a7023-48a9-498e-ab27-33800bcf22f6` | (-14, 2) | IN | OUT (0) |
| 136 | **Ø Window** | `7ec54364-46c2-4303-b6c8-66905802f3b3` | (-10, 2) | IN | OUT (0) |
| 137 | **Ø Wrap** | `55792b95-b570-4513-b89d-4057c1af338b` | (-6, 2) | IN | OUT (0) |
| 138 | **Phase-1** | `44da1c7d-5fef-4d7a-9b1c-739324a59a97` | (-2, 2) | PITCH_IN<br>PHASE_IN<br>GATE_IN | OUT (0) |
| 139 | **Phaser+** | `50a03b86-dac7-431a-b923-3ab687a54d03` | (2, 2) | IN<br>MOD_IN | OUT (0) |
| 140 | **Phasor** | `2944a921-f9af-4781-9cf7-7fe98218fce3` | (6, 2) | PITCH_IN<br>GATE_IN | OUT (0) |
| 141 | **Pinch** | `0df6f770-87b4-45fa-899b-d9e56c253255` | (10, 2) | IN | OUT (0) |
| 142 | **Pitch Buss** | `88a039b7-13d3-40c0-9977-bfe37d06c60f` | (14, 2) | IN<br>IN2<br>IN3<br>IN4<br>IN6<br>IN5 | OUT (0) |
| 143 | **Pitch Class** | `7e371fc4-dae1-426b-8f0b-6dd980e63d31` | (18, 2) | — | OUT (0) |
| 144 | **Pitch In** | `b5ce2b79-e881-4105-ad80-4435cc57f75e` | (22, 2) | — | OUT (0) |
| 145 | **Pitch Quantize** | `70a58062-9175-4eec-9a25-b8f0f919773b` | (26, 2) | IN | OUT (0) |
| 146 | **Pitch Scaler** | `c53fda13-4ed0-42fd-b410-19052ca6322d` | (30, 2) | IN | OUT (0) |
| 147 | **Pitch Shift** | `69d1a916-2d39-4a4f-9334-7ec4def8eb83` | (-30, 6) | PITCH_IN<br>PHASE_IN<br>IN<br>GRAIN_RATE_IN | OUT (0) |
| 148 | **Pitch → Freq** | `4ef26e44-92c8-42f0-a4fd-b70b3a3769cb` | (-26, 6) | IN | OUT (0) |
| 149 | **Pitch → Ø** | `f31bdee3-3f0c-4861-9a93-7514401a8a6f` | (-22, 6) | IN | OUT (0) |
| 150 | **Pitch** | `9adcd4b7-5dab-43cc-82da-ec5873ac3c72` | (-18, 6) | — | OUT (0) |
| 151 | **Pitches** | `c9b6cefc-c467-45b6-aedb-ba02a9f887fe` | (-14, 6) | PHASE_IN | OUT (0) |
| 152 | **Pluck** | `0ae4fef0-e859-4085-a100-448f5158eafb` | (-10, 6) | GATE_IN<br>IN | MOD_OUT (0)<br>OUT (1) |
| 153 | **Poly → Mono** | `0309fc67-0290-42b8-8ea3-625b333cb34c` | (-6, 6) | IN | OUT (0) |
| 154 | **Power** | `6808a887-6a5a-465d-ab48-84fb0995d2ca` | (-2, 6) | IN<br>IN2 | OUT (0) |
| 155 | **Pressure In** | `2f6804b9-87a8-4c06-a61b-31e4171e1f2d` | (2, 6) | — | OUT (0) |
| 156 | **Probabilities** | `a65c43a5-f59a-460a-b22f-88571ac380ec` | (6, 6) | PHASE_IN | OUT (0)<br>CONTROL_OUT (1) |
| 157 | **Product** | `93e8af3d-0cb4-41e4-b9cb-dc825b5fc5d7` | (10, 6) | IN<br>IN2<br>IN3<br>IN4<br>IN7<br>IN8<br>IN6<br>IN5 | OUT (0) |
| 158 | **Pulse** | `10c3be1f-ceb4-4bbc-bf35-af11285e58e0` | (14, 6) | PITCH_IN<br>PHASE_IN<br>GATE_IN | OUT (0) |
| 159 | **Push** | `b7573eb6-2902-4f89-98cf-2c33b9f1b43b` | (18, 6) | IN | OUT (0) |
| 160 | **Quantize** | `c1f45a63-edde-4c38-b588-efbd4c1e35ec` | (22, 6) | IN<br>MOD_IN | OUT (0)<br>REMAINDER (1) |
| 161 | **Quantizer** | `00e05a87-8b61-4540-9746-d8298406bc5a` | (26, 6) | IN | OUT (0) |
| 162 | **Rasp** | `3a06f9a2-b1ec-42ff-bb55-35b42fcff581` | (30, 6) | IN<br>MOD_IN | OUT (0) |
| 163 | **Ratio** | `7ab5e7c4-671e-40de-8c06-21dd273c908c` | (-30, 10) | PITCH_IN | OUT (0) |
| 164 | **Reciprocal** | `f4f35d7b-5fdd-40bd-98d8-c142e5ca66a8` | (-26, 10) | IN | OUT (0) |
| 165 | **Recorder** | `bdedc713-81ba-40b5-878c-a2e979ec2393` | (-22, 10) | IN<br>REC<br>PLAY | OUT (0) |
| 166 | **Rectifier** | `ac6de5ed-c143-4364-9989-3c7d299db380` | (-18, 10) | IN | OUT (0) |
| 167 | **Ripple** | `0b4317c5-7880-4515-ab71-b4607ddc8fdb` | (-14, 10) | IN<br>MOD_IN | OUT (0) |
| 168 | **Root Key** | `1bc70e1f-5d9d-407e-a087-e222ef63089e` | (-10, 10) | — | OUT (0) |
| 169 | **Roots** | `28166c20-3a55-45e8-8117-bfec9a62a4d4` | (-6, 10) | IN | OUT (0) |
| 170 | **Round** | `ae80ebb6-e84f-4cc9-848e-1dee19db8181` | (-2, 10) | IN | OUT (0)<br>REMAINDER (1) |
| 171 | **S/H LFO** | `965f7fc4-3f76-4e83-8870-98673cb0576a` | (2, 10) | RATE_IN<br>GATE_IN<br>PHASE_IN | OUT (0) |
| 172 | **SVF** | `2ddd3d4f-04b9-4ad5-a6f7-08e01df14c0f` | (6, 10) | IN<br>MOD_IN | OUT (0) |
| 173 | **Sallen-Key** | `726cd882-3d94-4140-b2b7-cfa7f416cc69` | (10, 10) | IN<br>MOD_IN | OUT (0) |
| 174 | **Sample / Hold** | `8214fd6c-5131-49d2-a9a6-709760a46b82` | (14, 10) | IN<br>GATE_IN | OUT (0) |
| 175 | **Sampler** | `40c0fe10-37ae-4d05-9ce1-d0bac5cd2b8e` | (18, 10) | VELOCITY_IN<br>GATE_IN<br>PITCH_IN | OUT (0)<br>ZONE_PARAM_1 (1)<br>ZONE_PARAM_2 (2)<br>ZONE_PARAM_3 (3) |
| 176 | **Saturator** | `267e71c5-6aad-41f6-92da-3127e3bd1a25` | (29, 10) | IN | OUT (0) |
| 177 | **Sawtooth** | `4ae6d37a-5412-4691-aa8b-261e94e60c59` | (26, 10) | PITCH_IN<br>PHASE_IN<br>GATE_IN | OUT (0) |
| 178 | **Scale Steps** | `0015d740-8c68-4576-834e-2d4dabef24e1` | (30, 10) | IN | OUT (0) |
| 179 | **Scrawl** | `9c1aa872-f271-4bd6-9f0d-37157399569c` | (-30, 14) | PITCH_IN<br>GATE_IN<br>PHASE_IN | OUT (0) |
| 180 | **Segments** | `953b71a0-c496-4cdc-8d50-843373d248b5` | (-26, 14) | PHASE_IN<br>IN<br>GATE_IN | OUT (0)<br>MOD_OUT (1) |
| 181 | **Select In** | `c6923eb3-e161-4eed-8a93-a4554287a77b` | (-22, 14) | IN<br>IN2<br>SEL | OUT (0) |
| 182 | **Select Out** | `4228f753-5073-4aa4-81c1-ec7f65b2ca23` | (-18, 14) | IN<br>SEL | OUT (0)<br>OUT2 (1) |
| 183 | **Shift Register** | `749fc1c8-9f66-43bb-b11d-fbd7e5e84c02` | (-14, 14) | GATE_IN<br>IN | OUT (0)<br>OUT2 (1)<br>OUT3 (2)<br>OUT4 (3)<br>OUT7 (4)<br>OUT6 (5)<br>OUT8 (6)<br>OUT5 (7) |
| 184 | **Shred** | `cd8d3ec5-9655-4f5f-9a45-5aaf87edaa57` | (-10, 14) | IN | OUT (0) |
| 185 | **Sine** | `ca05aebd-ecaf-4d57-b0f6-c04ce81674c4` | (-6, 14) | PITCH_IN<br>PHASE_IN<br>GATE_IN | OUT (0) |
| 186 | **Slope ↗** | `4da936f3-c96b-43f6-b716-6a70407a38fc` | (-2, 14) | IN | OUT (0) |
| 187 | **Slope ↘** | `78e296cf-9ac8-415a-96c3-b7e924e061f3` | (2, 14) | IN | OUT (0) |
| 188 | **Slopes** | `0b754e8c-cfb6-4399-aabe-c23d7e635f72` | (6, 14) | PHASE_IN | OUT (0) |
| 189 | **Soar** | `d7ca54e4-1d83-4dec-a40e-14d40fbd5ab5` | (10, 14) | IN | OUT (0) |
| 190 | **Spectrum** | `9fe38e12-614b-470c-9dde-789fbde43f30` | (14, 14) | IN<br>IN2<br>IN3<br>IN4 | — |
| 191 | **Split** | `61968cb5-c43f-41ce-bbb9-07e649dc38a5` | (18, 14) | MOD_IN<br>IN | OUT (0)<br>OUT2 (1)<br>OUT3 (2)<br>OUT4 (3)<br>OUT7 (4)<br>OUT6 (5)<br>OUT8 (6)<br>OUT5 (7) |
| 192 | **Step Access** | `c74b57ac-0295-4daf-979a-b6248efbde7c` | (22, 14) | — | OUT (0) |
| 193 | **Steps** | `80d4de64-0ebc-4bb8-b448-74e57240f4a9` | (26, 14) | PHASE_IN | OUT (0) |
| 194 | **Stereo Merge** | `36096881-77f5-4ce1-b8c5-b3b21e6440f3` | (30, 14) | IN<br>IN2<br>IN3<br>IN4 | OUT (0) |
| 195 | **Stereo Split** | `842ae87e-de89-4583-9f24-43b91a218d1f` | (-30, 18) | IN | OUT (0)<br>OUT2 (1)<br>OUT3 (2)<br>OUT4 (3) |
| 196 | **Stereo Width** | `a34edcba-25b3-4f07-86b2-81701b092d66` | (-26, 18) | IN | OUT (0) |
| 197 | **Sub** | `d1263096-fddf-438f-9c9f-ed9c1693e954` | (-22, 18) | PITCH_IN<br>GATE_IN | OUT (0) |
| 198 | **Subtract** | `1c779472-00d1-459c-9532-6b01d3baab1a` | (-18, 18) | IN<br>IN2 | OUT (0) |
| 199 | **Sum** | `5b414321-7adb-4210-ab26-d2367a8b5d56` | (-14, 18) | IN<br>IN2<br>IN3<br>IN4<br>IN7<br>IN8<br>IN6<br>IN5 | OUT (0) |
| 200 | **Swarm** | `faea6af4-72db-42c6-adac-0f74d8ebdbbf` | (-10, 18) | PITCH_IN<br>PHASE_IN<br>GATE_IN | OUT (0) |
| 201 | **Timbre In** | `21a6a402-2611-4311-b372-f36d36ad25d8` | (-6, 18) | — | OUT (0) |
| 202 | **Toggle In** | `168a4502-2ec0-4222-b6cb-5a01875bc543` | (-2, 18) | IN<br>IN2 | OUT (0) |
| 203 | **Toggle Out** | `f75deac4-c3d0-4630-a09c-4bbdac03c9d3` | (2, 18) | IN | OUT (0)<br>OUT2 (1) |
| 204 | **Toggle** | `5d016b16-be9c-4735-b9df-a533ee72528b` | (6, 18) | IN | OUT (0) |
| 205 | **Transfer** | `3b18c07d-c4cb-4195-9c85-6b37ca1c048a` | (10, 18) | IN | OUT (0) |
| 206 | **Transport Playing** | `9714df20-f4ea-4017-a874-4ccb554dd86e` | (14, 18) | — | OUT (0) |
| 207 | **Transport** | `997869ea-e649-4ac8-865e-bd4ac9e7b2a2` | (18, 18) | — | OUT (0)<br>GATE_OUT (1) |
| 208 | **Transpose** | `35de4fbc-95f6-4719-911a-bc81a2d48df4` | (22, 18) | IN | OUT (0) |
| 209 | **Triangle** | `9ab5d37c-f1ae-47a0-b85d-0f5b7c4fdb90` | (26, 18) | PITCH_IN<br>PHASE_IN<br>GATE_IN | OUT (0) |
| 210 | **Trigger** | `d6aa9f53-8cc6-45a5-8fc7-f4ba97274b77` | (30, 18) | IN | OUT (0) |
| 211 | **Triggers** | `e75916a0-2594-4181-88a4-b19fdb77c0eb` | (-30, 22) | IN | OUT (0) |
| 212 | **Uni → Bi** | `9d4c07ec-ea76-4c30-8c4e-ab94a192ec43` | (-26, 22) | IN | OUT (0) |
| 213 | **Union** | `df0a08cc-68b4-4fb2-a662-05cb09745e37` | (-22, 22) | PITCH_IN<br>PHASE_IN<br>GATE_IN | OUT (0) |
| 214 | **VU Meter** | `08d55d78-9240-43b9-9fe3-acde57ac1e60` | (-18, 22) | IN | OUT (0) |
| 215 | **Value Readout** | `8ac47e6d-1f50-41c0-91d1-0e4fa33e2f52` | (-14, 22) | IN | — |
| 216 | **Value Scaler** | `512afe2b-0065-46b2-a65f-c8524b9e3552` | (-10, 22) | IN | OUT (0) |
| 217 | **Value** | `1faa5baf-6cdf-406a-b0e4-89b67501d982` | (-6, 22) | — | OUT (0) |
| 218 | **Velo Mult** | `e74a80e4-9c17-49a8-9e84-98d07d6187bb` | (-2, 22) | IN | OUT (0) |
| 219 | **Velocity In** | `1ab8dfab-0671-406c-a423-5f362f5a62ca` | (2, 22) | — | OUT (0) |
| 220 | **Voice Stack Info** | `7a8675a4-be5a-4393-9257-c10b25358bfa` | (6, 22) | — | STACK_INDEX (0)<br>STACK_SIZE (1) |
| 221 | **Voice Stack Mix** | `d58ced40-e61d-4988-8321-3a3456cdfe15` | (10, 22) | IN | OUT (0) |
| 222 | **Voice Stack Tog** | `b96d7a4a-d0c8-4d4e-b069-98908e1fa2ea` | (14, 22) | IN | OUT (0) |
| 223 | **Vowels** | `b4c661b9-576e-46ac-8be2-4974dd2f40ce` | (18, 22) | IN<br>MOD_IN<br>VOWEL_IN | OUT (0) |
| 224 | **Wavefolder** | `aef23bda-40b6-4dba-86f5-044f617574e4` | (22, 22) | IN | OUT (0) |
| 225 | **Wavetable LFO** | `d2524378-5019-40e7-af9f-08ec6aafce7e` | (26, 22) | RATE_IN<br>GATE_IN<br>PHASE_IN<br>TABLE_IN | OUT (0) |
| 226 | **Wavetable** | `19749bf6-0974-4356-9bce-6ab3b5a1af04` | (30, 22) | PITCH_IN<br>PHASE_IN<br>GATE_IN<br>TABLE_IN | OUT (0) |
| 227 | **XNOR** | `c533df98-a287-4bdb-b1d9-1a694470721b` | (-30, 26) | IN<br>IN2 | OUT (0) |
| 228 | **XOR** | `e6254ddf-6ba9-47f5-a6ac-402e2fc29a6c` | (-26, 26) | IN<br>IN2 | OUT (0) |
| 229 | **XP** | `6cccc56b-cd93-435d-bae0-4d10c35c387a` | (-22, 26) | IN<br>MOD_IN | OUT (0) |
| 230 | **XY** | `e84c96bc-6ff3-401b-af14-eddf9344c3e9` | (-18, 26) | — | OUT (0)<br>OUT2 (1) |
| 231 | **Zero Crossings** | `5ff7e6e8-5158-46d4-9ba5-2d412750334c` | (-14, 26) | IN | OUT (0) |
| 232 | **by Scale** | `fc4504c5-73ec-4914-af09-6cb05bf9fccf` | (-10, 26) | IN | OUT (0) |
| 233 | **by Semitone** | `845ff7e3-5e5b-4ffc-a8c7-531907e4709e` | (-6, 26) | IN | OUT (0) |
| 234 | **dB → Lin** | `20cd7bb0-81b2-444d-9b5c-49cf5aa2f341` | (-2, 26) | IN | OUT (0) |

## Per-device parameter inventory

Each of the 232 catalog packages is represented by the first matching graph instance. The JSON file also retains all duplicate instances and their exact graph state.

| Device | Package ID | Instance | Parameters (native range/options/display) |
| --- | --- | ---: | --- |
| **AD** | `5b7ab937-4f09-41fc-a379-983fb597b2ff` | 3 | `ATTACK (float); value=0.271714286; range=[0, 2]; display=20.1 ms`<br>`DECAY (float); value=0.694; range=[0, 2]; display=334 ms`<br>`ENVELOPE (integer); metadata unavailable`<br>`GATE (boolean); value=true; options=false, true; display=On`<br>`DECAY_CURVE (float); value=-1; range=[-1, 1]; display=-100 %`<br>`ATTACK_CURVE (float); value=0.5; range=[-1, 1]; display=50.0 %`<br>`AFFECT_VOICE_LIFETIME (boolean); value=true; options=false, true; display=On`<br>`LOOP (boolean); value=false; options=false, true; display=Off`<br>`MODEL (integer); options=0:Analog, 1:Relative, 2:Digital; display=Digital` |
| **ADSR** | `7e09068b-fee5-457e-afe4-7017661ebbd3` | 1 | `ATTACK (float); value=0.221714286; range=[0, 2]; display=10.9 ms`<br>`DECAY (float); value=0.944; range=[0, 2]; display=841 ms`<br>`SUSTAIN (float); value=0.535; range=[0, 1]; display=53.5 %`<br>`RELEASE (float); value=0.625101714; range=[0, 2]; display=244 ms`<br>`ENVELOPE (integer); metadata unavailable`<br>`GATE (boolean); value=true; options=false, true; display=On`<br>`IN (boolean); options=false, true`<br>`ATTACK_CURVE (float); value=0.5; range=[-1, 1]; display=50.0 %`<br>`DECAY_CURVE (float); value=-1; range=[-1, 1]; display=-100 %`<br>`RELEASE_CURVE (float); value=-1; range=[-1, 1]; display=-100 %`<br>`AFFECT_VOICE_LIFETIME (boolean); value=true; options=false, true; display=On`<br>`MODEL (integer); options=0:Analog, 1:Relative, 2:Digital; display=Digital` |
| **AM/RM** | `e1d4fdf5-057e-4c83-869e-db4ee322e4ce` | 5 | `DEPTH (float); value=0.5; range=[0, 1]; display=50.0 %` |
| **AND** | `1e330c79-9a6f-4015-8dfa-da507c1bb15a` | 6 | — |
| **AR** | `9eaf8e7d-b8f7-4134-85c1-c7c77dd9fe92` | 7 | `ATTACK (float); value=0.271714286; range=[0, 2]; display=20.1 ms`<br>`RELEASE (float); value=0.629960525; range=[0, 2]; display=250 ms`<br>`ENVELOPE (integer); metadata unavailable`<br>`GATE (boolean); value=true; options=false, true; display=On`<br>`RELEASE_CURVE (float); value=-1; range=[-1, 1]; display=-100 %`<br>`ATTACK_CURVE (float); value=0.5; range=[-1, 1]; display=50.0 %`<br>`AFFECT_VOICE_LIFETIME (boolean); value=true; options=false, true; display=On`<br>`MODEL (integer); options=0:Analog, 1:Relative, 2:Digital; display=Digital` |
| **Abs** | `895470df-c2de-417f-9113-8bb6fe948b6d` | 8 | — |
| **Accents** | `a0b3bd86-a4a9-4eac-83fc-468840332778` | 9 | `STEPS (integer); value=8; range=[2, 64]; display=8`<br>`DEVICE_PHASE (boolean); value=true; options=false, true; display=On`<br>`MUTE_WHEN_STOPPED (boolean); value=false; options=false, true; display=Off`<br>`MODE (integer); options=0:Gate, 1:Pulse, 2:Trigger; display=Trigger`<br>`FLIP_TRIGGER (boolean); options=false, true`<br>`NUDGE_LEFT (boolean); options=false, true`<br>`NUDGE_RIGHT (boolean); options=false, true`<br>`RANDOM_TRIGGER (boolean); options=false, true` |
| **Add** | `57a6f72c-db9d-4a96-bc4b-d6a2bb8b656a` | 10 | — |
| **All-pass Delay** | `f435652c-2fd7-4edd-8b7a-ee97b0fd43a5` | 11 | `TIME (float); value=0.033; range=[0, 0.999]; display=33.0 ms`<br>`GAIN (float); value=0.761; range=[0, 1]; display=76.1 %` |
| **All-pass** | `b1682757-4fcf-4b5f-bfe7-58dd81d79954` | 12 | `CUTOFF (float); value=102.232645; range=[15, 144]; display=3.00 kHz`<br>`POLES (integer); options=0:1ᴾ, 1:2ᴾ, 2:3ᴾ, 3:4ᴾ, 4:5ᴾ, 5:6ᴾ; display=6ᴾ` |
| **Amplify** | `a6cd650b-c4de-46c6-8741-c07a0a9bfec2` | 13 | `VALUE (boolean); value=1; options=false, true; display=100 %`<br>`STEREOIZE (boolean); value=false; options=false, true; display=Off` |
| **Array** | `010ba490-caf6-4af6-93bd-82d9be63610c` | 14 | `COUNT (integer); value=16; range=[2, 1024]; display=16`<br>`NORMALIZE (boolean); value=true; options=false, true; display=On` |
| **Attenuate** | `cfc56753-defc-4324-8a68-bf747ff45508` | 15 | `VALUE (boolean); value=1; options=false, true; display=100 %`<br>`STEREOIZE (boolean); value=false; options=false, true; display=Off` |
| **Audio In** | `b2a6b111-7afd-4c95-b380-6de8125af980` | 16 | — |
| **Audio Out** | `af7b5503-c955-489e-9461-164107d56bb6` | 2 | `IN (boolean); options=false, true`<br>`AFFECT_VOICE_LIFETIME (boolean); value=false; options=false, true; display=Off`<br>`SILENCE_THRESHOLD (float); value=-96; range=[-144, 0]; display=-96.0 dB`<br>`HOLD_TIME (float); value=0.05; range=[0, 1]; display=50.0 ms`<br>`CLIP_MODE (integer); options=0:Off, 1:Hard, 2:Soft (legacy), 3:Soft; display=Soft`<br>`CLIP_LEVEL (integer); options=0:0 dB, 1:+6 dB, 2:+12 dB, 3:+24 dB; display=+24 dB` |
| **Audio Sidechain** | `59a10d46-c6a2-4676-a0fb-8a2923636d82` | 18 | — |
| **Average** | `2cbbf968-2a51-48ab-9e1f-ba665a52ea8b` | 19 | `TIME (float); value=-1.523; range=[-5, 2]; display=30.0 ms` |
| **Bend** | `c7d55e0b-33c6-4436-ba37-d1f1a0953893` | 20 | `BEND (float); value=0; range=[-1, 1]; display=0.00 %`<br>`STEREOIZE (boolean); value=false; options=false, true; display=Off` |
| **Bi → Uni** | `97f5eff7-7619-4957-aa8f-5cfc353d56d6` | 21 | — |
| **Bias** | `c5aee529-9dce-406d-87cd-0f1cabcac13f` | 22 | `VALUE (boolean); value=0; options=false, true; display=0.00 %`<br>`STEREOIZE (boolean); value=false; options=false, true; display=Off` |
| **Bite** | `18b292a7-c11c-4014-b563-0784601e7cc8` | 23 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`OSC_A_LEVEL (float); value=1; range=[0, 1]; display=100 %`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`OSC_B_LEVEL (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`OSC_A_PW (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`OSC_B_PW (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`OSC_A_SHAPE (integer); options=0:Sine, 1:Saw, 2:Pulse, 3:Triangle To Saw, 4:Ramped Pulse, 5:Shark Tooth, 6:Hoover, 7:Saw to Square, 8:Dual Saw; display=Dual Saw`<br>`OSC_B_SHAPE (integer); options=0:Sine, 1:Saw, 2:Pulse, 3:Triangle To Saw, 4:Ramped Pulse, 5:Shark Tooth, 6:Hoover, 7:Saw to Square, 8:Dual Saw; display=Dual Saw`<br>`OSC_B_FM (float); value=12; range=[0, 102]; display=+12.00 st`<br>`OSC_A_PWM (float); value=0; range=[0, 1]; display=0.00 %`<br>`OSC_B_SYNC (boolean); value=true; options=false, true; display=On`<br>`OSC_B_PITCH (float); value=17; range=[-48, 84]; display=+17.00 st`<br>`RING_LEVEL (float); value=0; range=[0, 1]; display=0.00 %`<br>`MONO_MODE (boolean); value=false; options=false, true; display=Off` |
| **Blend** | `0f2a027d-2bc3-4789-8a56-4d079a7e6137` | 24 | `DEPTH (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`MODE (integer); options=0:Equal Gain, 1:Equal Power; display=Equal Power` |
| **Button** | `c0281e6e-3d55-4e86-8c9b-0ce8cf3db67d` | 25 | `VALUE (boolean); value=false; options=false, true; display=Off`<br>`BIPOLAR (boolean); value=false; options=false, true; display=Off` |
| **CC In** | `311f3697-7323-46a0-a00b-1c51b12042e9` | 26 | `SMOOTH (boolean); value=true; options=false, true; display=On`<br>`CC1 (integer); value=1; range=[0, 127]; display=CC 1`<br>`MIDI_CHANNEL (integer); value=0; range=[0, 16]; display=0`<br>`LEARN (boolean); options=false, true` |
| **CC Out** | `131d870c-0df7-4f28-a536-cd13e82af404` | 27 | `CC1 (integer); value=1; range=[0, 127]; display=CC 1`<br>`MIDI_CHANNEL (integer); value=1; range=[1, 16]; display=Ch 1`<br>` (boolean); options=false, true` |
| **CV In** | `632c2ab7-5c5a-493a-af69-ba4ada9997eb` | 28 | `RATE (float); value=135; range=[-36.42, 135]; display=19.9 kHz`<br>`GAIN (float); value=0; range=[-24, 24]; display=0.0 dB`<br>`MODE (integer); options=0:AC, 1:DC; display=DC` |
| **CV Out** | `f137c16d-d9a3-471d-9e1d-586722988695` | 29 | `SMOOTH (float); value=-3; range=[-3, 0]; display=1.00 ms`<br>`MODE (integer); options=0:AC, 1:DC; display=DC` |
| **CV Pitch In** | `cc87d3c3-46f5-41e3-91d9-882243cdf717` | 30 | `RATE (float); value=135; range=[-36.42, 135]; display=19.9 kHz`<br>`MODE (integer); options=0:AC, 1:DC; display=DC`<br>`RANGE (float); value=10; range=[1, 15]; display=10.00`<br>`ROOT_KEY (integer); value=60; range=[0, 127]; display=60` |
| **CV Pitch Out** | `502771b2-1a4f-44c4-9038-03cac7da59e7` | 31 | `SMOOTH (float); value=-3; range=[-3, 0]; display=1.00 ms`<br>`MODE (integer); options=0:AC, 1:DC; display=DC`<br>`RANGE (float); value=10; range=[1, 15]; display=10.00`<br>`ROOT_KEY (integer); value=60; range=[0, 127]; display=60` |
| **Ceil** | `321563fe-42e4-4353-84e2-bd95db6a00e4` | 32 | — |
| **Chance** | `fe6be8de-5abf-4825-99d7-c2127f039bb4` | 33 | `PROBABILITY (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`NOTE_TRIGGER (boolean); value=false; options=false, true; display=Off` |
| **Chebyshev** | `0b9d73b3-796f-4cc0-b7af-d59e19df2827` | 34 | `ORDER (float); value=3; range=[1, 32]; display=3.00`<br>`NO_DC (boolean); value=false; options=false, true; display=Off` |
| **Chorus+** | `537b38d0-8ad3-4fa0-aa24-82c7c56c3d21` | 35 | `TYPE (integer); options=0:CE, 1:DD, 2:8v, 3:x2; display=x2`<br>`Y (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`X (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`RATE (float); value=0.3333333; range=[0, 1]; display=33.3 %`<br>`DEPTH (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`MIX (float); value=0.5; range=[0, 1]; display=50.0 %` |
| **Clip** | `d9309744-b38c-4f40-95de-ee56bb073f4e` | 36 | `LEVEL (float); value=0; range=[-96, 0]; display=0.0 dB` |
| **Clock Divide** | `a072e864-32de-4c4c-a334-2ed9afab0965` | 37 | `STEPS (integer); value=2; range=[1, 64]; display=2` |
| **Clock Quantize** | `86d811e8-e1df-470b-9740-3bf3d924d87a` | 38 | `TRIGGER (boolean); value=false; options=false, true; display=Off` |
| **Clock** | `245af7f8-1137-4b44-abc3-b5e1f52fe016` | 39 | `RATE (float); value=1; range=[0, 32]; display=1.00 Hz`<br>`RETRIGGER (boolean); value=true; options=false, true; display=On` |
| **Comb** | `b84241c5-b8b7-403f-8422-8195cf6d3478` | 40 | `CUTOFF (float); value=60; range=[15, 144]; display=262 Hz`<br>`DECAY (float); value=0.156322366; range=[0, 2]; display=3.82 ms`<br>`POLARITY (integer); options=0:Positive, 1:Negative; display=Negative`<br>`KEYTRACK (float); value=1; range=[0, 2]; display=100 %`<br>`CUTOFF_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`DAMPING (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`Q_LIMIT (float); value=-10; range=[-30, 12]; display=-10.0 dB` |
| **Comment** | `b297dabd-144e-4106-b8da-15d08fa6b124` | 41 | — |
| **Constant** | `5412a6f2-9920-41b5-af13-ea64d266a26d` | 42 | `VALUE (float); value=1; range=[-999999, 999999]; display=1.00` |
| **Crossover-2** | `6ecd5ea8-9105-4350-af41-b2870ca54364` | 43 | `CUTOFF (float); value=84; range=[15, 144]; display=1.05 kHz` |
| **Crossover-3** | `979bec96-fea9-4d7d-9657-65a447709b50` | 44 | `CUTOFF (float); value=60; range=[15, 144]; display=262 Hz`<br>`CUTOFF2 (float); value=108; range=[15, 144]; display=4.19 kHz` |
| **Curve** | `1093d01f-f6ba-4eef-8a62-3409d4d365ab` | 45 | `LOW_IN (float); value=-0.5; range=[-1, 1]; display=-50.0 %`<br>`HIGH_IN (float); value=0.5; range=[-1, 1]; display=50.0 %`<br>`LOW (float); value=-0.5; range=[-1, 1]; display=-50.0 %`<br>`HIGH (float); value=0.75; range=[-1, 1]; display=75.0 %`<br>`BEND (float); value=-0.201015315; range=[-1, 1]; display=-20.1 %` |
| **Curves** | `2302d0d8-afc0-4ed6-86ef-6d1dffeda6a2` | 46 | `RATE_MOD (float); value=0; range=[-32, 32]; display=0.00`<br>`RETRIGGER (boolean); value=true; options=false, true; display=On`<br>`TIMEBASE (integer); options=0:Hertz, 1:Kilohertz, 2:Bar, 3:Half note, 4:Quarter note, 5:8th note, 6:16th note, 7:32nd note, 8:Dotted half note, 9:Dotted quarter note, 10:Dotted 8th note, 11:Dotted 16th note, 12:Dotted 32nd note, 13:Triplet half note, 14:Triplet quarter note, 15:Triplet 8th note, 16:Triplet 16th note, 17:Triplet 32nd note, 18:Hold; display=Hold`<br>`RATE (float); value=1; range=[0, 32]; display=1.00`<br>`PHASE (float); value=0; range=[-360, 360]; display=0 °`<br>`LFO (integer); metadata unavailable`<br>`PHASE_MOD (float); value=0; range=[0, 1]; display=0.00`<br>`RPHASE (float); value=0; range=[-360, 360]; display=0 °`<br>`CURVE (boolean); options=false, true`<br>`TIME (float); value=-2; range=[-5, 1]; display=10.0 ms`<br>`ENABLE_SMOOTH (boolean); value=true; options=false, true; display=On`<br>`TRANSPORT_SYNC (boolean); value=false; options=false, true; display=Off` |
| **Delay** | `e2e808c8-6b7e-4a00-9563-39e2f44177da` | 47 | `TIME (float); value=0.5; range=[0, 1]; display=125 ms` |
| **Dice** | `9f66c3b9-ca9b-4b62-8792-73fbec6464a4` | 48 | `NOTE_TRIGGER (boolean); value=false; options=false, true; display=Off`<br>`BIPOLAR (boolean); value=false; options=false, true; display=Off` |
| **Diode** | `8399cc4f-57a6-48aa-a38b-2dac60fd15f8` | 49 | `DRIVE (float); value=0; range=[0, 40]; display=0.0 dB`<br>`AA (boolean); value=true; options=false, true; display=On`<br>`LOW_PASS (float); value=120; range=[0, 144]; display=8.37 kHz`<br>`BIAS (float); value=0; range=[-0.99, 0.99]; display=0.00 %` |
| **Distortion** | `6e8f9374-3393-4531-9f7e-571d0033ea94` | 50 | `DRIVE (float); value=0; range=[0, 40]; display=0.0 dB`<br>`AA (boolean); value=true; options=false, true; display=On` |
| **Divide** | `21a1b455-fa76-4662-ad31-e89fbe0fcd65` | 51 | — |
| **Dome** | `fa194943-ad9a-4106-9aa9-9e2df5e44593` | 52 | `MODE (integer); options=0:Rough, 1:Normal, 2:Better, 3:Excellent; display=Excellent` |
| **=** | `e4fda749-9129-4f03-ba7a-06099575ced6` | 53 | `EXACT (boolean); value=false; options=false, true; display=Off` |
| **Exp** | `eca1e042-b7ac-4f9e-863d-e5f32f6755da` | 54 | `BASE (integer); options=0:2, 1:e, 2:10; display=10` |
| **Exponents** | `0ef176bd-a46a-424f-a163-2fc2276a9779` | 55 | `EXPONENT (integer); value=2; range=[-9, 9]; display=2` |
| **Fizz** | `d9e01995-14fc-4bae-a727-0fe2aa40c338` | 56 | `CUTOFF2 (float); value=84; range=[15, 144]; display=1.05 kHz`<br>`KEYTRACK (float); value=1; range=[0, 2]; display=100 %`<br>`CUTOFF_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`CUTOFF (float); value=96; range=[15, 144]; display=2.09 kHz`<br>`FBK_GAIN (float); value=0.4; range=[0, 1]; display=40.0 %`<br>`COLOR (float); value=0.34; range=[-1, 1]; display=34.0 %`<br>`MODE (boolean); value=false; options=false, true; display=Off` |
| **Flanger+** | `00b09256-db30-40d5-b94f-c22477e49b5c` | 57 | `TYPE (integer); options=0:DP, 1:MX, 2:TFX, 3:WA; display=WA`<br>`STEREO (boolean); value=true; options=false, true; display=On`<br>`INVERT (boolean); value=false; options=false, true; display=Off`<br>`DIRTY (boolean); value=false; options=false, true; display=Off`<br>`CENTER (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`FEEDBACK (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`RATE (float); value=-0.301; range=[-3, 1]; display=0.50 Hz`<br>`DEPTH (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`MIX (float); value=0.5; range=[0, 1]; display=50.0 %` |
| **Floor** | `b0f4c3b2-eae2-44b3-805b-9d8d4c45ee34` | 58 | — |
| **Follower RF** | `0a1490cc-7df2-470c-b48e-6889b0f0361b` | 59 | `ATTACK (float); value=-2.304; range=[-4, 1]; display=4.97 ms`<br>`DECAY (float); value=-0.376; range=[-4, 1]; display=421 ms`<br>`ENVELOPE (integer); metadata unavailable`<br>`MODE (integer); options=0:Peak, 1:RMS; display=RMS` |
| **Follower** | `165fd92f-ed5e-4a54-97ed-99f334e28801` | 60 | `TIME (float); value=-1.456; range=[-4, 1]; display=35.0 ms`<br>`RMS (boolean); value=false; options=false, true; display=Off` |
| **Freq Shift+** | `904717d9-f24e-4742-9c75-b61ca0bf97bd` | 61 | `RATE_MOD (float); value=0; range=[-32, 32]; display=0.00`<br>`TIMEBASE (integer); options=0:Hertz, 1:Kilohertz, 2:Bar, 3:Half note, 4:Quarter note, 5:8th note, 6:16th note, 7:32nd note, 8:Dotted half note, 9:Dotted quarter note, 10:Dotted 8th note, 11:Dotted 16th note, 12:Dotted 32nd note, 13:Triplet half note, 14:Triplet quarter note, 15:Triplet 8th note, 16:Triplet 16th note, 17:Triplet 32nd note, 18:Hold, 19:Keytrack; display=Keytrack`<br>`RATE (float); value=0.1; range=[0.02, 50]; display=0.10`<br>`PHASE (float); value=0; range=[-360, 360]; display=0 °`<br>`PHASE_MOD (float); value=0; range=[0, 1]; display=0.00 %`<br>`RPHASE (float); value=0; range=[-360, 360]; display=0 °`<br>`CENTER (float); value=0; range=[-1, 1]; display=0.00 %`<br>`FEEDBACK (float); value=0; range=[-1, 1]; display=0.00 %`<br>`FBUD (float); value=1; range=[-1, 1]; display=100 %`<br>`DELAYTIME (float); value=0.5; range=[0, 1]; display=125 ms`<br>`MIX (float); value=1; range=[0, 1]; display=100 %`<br>`LOPASS (float); value=140; range=[1, 145]; display=26.6 kHz`<br>`HIPASS (float); value=1; range=[1, 138]; display=8.66 Hz`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`EXTRA_PHASE (boolean); value=false; options=false, true; display=Off`<br>`ANTIREFLECTION (boolean); value=false; options=false, true; display=Off`<br>`MODE (integer); options=0:Rough, 1:Normal, 2:Better, 3:Excellent; display=Excellent`<br>`USE_DELAY (boolean); value=false; options=false, true; display=Off` |
| **Freq → Pitch** | `fc1fba88-7413-41a4-9427-7251a44ac040` | 62 | `UNIT (integer); options=0:Hertz, 1:Kilohertz; display=Kilohertz`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz` |
| **Gain - Vol** | `b1296326-cbf0-4797-9fc6-e2a6f2ce4a78` | 63 | `DRIVE (float); value=1; range=[0, 2]; display=0.0 dB` |
| **Gain - dB** | `b2c6ef93-8a14-4e10-b152-56bcee883e1c` | 64 | `GAIN (float); value=0; range=[-24, 24]; display=0.0 dB` |
| **Gain In** | `e470fc3b-4979-4c3b-aa79-27e6c49a3b88` | 65 | `SMOOTH (boolean); value=true; options=false, true; display=On` |
| **Gate In** | `4e00fda6-20f6-45a9-9d7e-02867cf09b82` | 66 | `AFFECT_VOICE_LIFETIME (boolean); value=false; options=false, true; display=Off` |
| **Gate Length** | `7b001029-62eb-4c40-81ab-13828622f3fd` | 67 | `LENGTH (float); value=-1.30103; range=[-4, 1]; display=50.0 ms` |
| **Gate Repeat** | `71508287-dc35-4e62-b1a0-82ba2a2d8ef7` | 68 | `RATE (float); value=-1.30103; range=[-4, 1]; display=50.0 ms` |
| **Gates** | `8d644ad7-8d77-4f05-a36e-04a57f719635` | 69 | `STEPS (integer); value=8; range=[2, 64]; display=8`<br>`DEVICE_PHASE (boolean); value=true; options=false, true; display=On`<br>`MUTE_WHEN_STOPPED (boolean); value=false; options=false, true; display=Off`<br>`MODE (integer); options=0:Gate, 1:Pulse, 2:Trigger; display=Trigger`<br>`FLIP_TRIGGER (boolean); options=false, true`<br>`NUDGE_LEFT (boolean); options=false, true`<br>`NUDGE_RIGHT (boolean); options=false, true`<br>`RANDOM_TRIGGER (boolean); options=false, true` |
| **≥** | `d6008d9a-57b1-416a-ae5c-795dd386c674` | 70 | `EXACT (boolean); value=true; options=false, true; display=On` |
| **>** | `7b681143-c276-49b9-9fed-1ce51d33aa39` | 71 | — |
| **HW In** | `d8195834-0238-4a18-bcba-d79efafa6f25` | 72 | — |
| **HW Out** | `49f0844b-e202-4011-b0a4-0d9f7c2ff41e` | 73 | — |
| **Hard Clip** | `5ae67be0-65a0-4905-84b4-1908baaf5613` | 74 | `DRIVE (float); value=0; range=[0, 40]; display=0.0 dB`<br>`AA (boolean); value=true; options=false, true; display=On` |
| **Heat** | `cc13faed-d9c5-47b5-aca6-d0adbe0afdb5` | 75 | `DRIVE (float); value=0; range=[0, 40]; display=0.0 dB`<br>`AA (boolean); value=true; options=false, true; display=On` |
| **High-pass** | `052cbe38-8ace-4ded-a4a9-de80a9f5fcea` | 76 | `CUTOFF (float); value=84; range=[15, 144]; display=1.05 kHz`<br>`POLES (integer); options=0:1ᴾ, 1:2ᴾ, 2:3ᴾ, 3:4ᴾ, 4:5ᴾ, 5:6ᴾ; display=6ᴾ` |
| **Hold** | `9671cb0e-7272-4d50-9d2e-a207971983cf` | 77 | — |
| **Howl** | `5d528874-cf9f-48e8-9386-b3118a38d279` | 78 | `DRIVE (float); value=0; range=[0, 40]; display=0.0 dB`<br>`AA (boolean); value=true; options=false, true; display=On` |
| **Invert** | `378e9b7d-0b95-4032-a12a-36d345550fab` | 79 | `STEREONESS (integer); options=0:Left, 1:Mono, 2:Right; display=Right`<br>`INVERT (boolean); value=true; options=false, true; display=On` |
| **Key On** | `6ba4eb9c-3ac6-4246-a4bd-192d395a3a58` | 80 | `MIDI_KEY (integer); value=36; range=[0, 127]; display=36`<br>`MIDI_CHANNEL (integer); value=0; range=[0, 16]; display=0`<br>`LEARN (boolean); options=false, true` |
| **Keys Held** | `ea6c6b9d-831b-4c05-a26b-2b1dadf81e0e` | 81 | — |
| **LFO** | `b89c1bce-203a-46be-8869-a44eb7868860` | 82 | `RATE_MOD (float); value=0; range=[-32, 32]; display=0.00`<br>`RETRIGGER (boolean); value=true; options=false, true; display=On`<br>`BIPOLAR (boolean); value=false; options=false, true; display=Off`<br>`WAVE (integer); options=0:Triangle, 1:Pulse, 2:Sine, 3:Teeth; display=Teeth`<br>`SKEW (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`TIMEBASE (integer); options=0:Hertz, 1:Kilohertz, 2:Bar, 3:Half note, 4:Quarter note, 5:8th note, 6:16th note, 7:32nd note, 8:Dotted half note, 9:Dotted quarter note, 10:Dotted 8th note, 11:Dotted 16th note, 12:Dotted 32nd note, 13:Triplet half note, 14:Triplet quarter note, 15:Triplet 8th note, 16:Triplet 16th note, 17:Triplet 32nd note, 18:Hold; display=Hold`<br>`RATE (float); value=1; range=[0, 32]; display=1.00`<br>`PHASE (float); value=0; range=[-360, 360]; display=0 °`<br>`LFO (integer); metadata unavailable`<br>`PHASE_MOD (float); value=0; range=[0, 1]; display=0.00 %`<br>`RPHASE (float); value=0; range=[-360, 360]; display=0 °`<br>`TRANSPORT_SYNC (boolean); value=false; options=false, true; display=Off` |
| **LR Gain** | `6a9e4b04-0e24-424f-abe3-a23b0744319a` | 83 | `LEFT (float); value=1; range=[-2, 2]; display=100 %`<br>`RIGHT (float); value=1; range=[-2, 2]; display=100 %` |
| **Label** | `b3a19e19-da13-491d-b569-16ff5cbb109b` | 84 | — |
| **Lag** | `a4d23895-2761-476b-9aad-cbe372d286ea` | 85 | `TIME (float); value=-1.301; range=[-5, 2]; display=50.0 ms` |
| **Latch** | `61810948-1f33-4bc5-a8bb-d30c78e0afde` | 86 | — |
| **≤** | `a5080bc6-2ee1-4a97-ad52-511f2a88343f` | 87 | `EXACT (boolean); value=true; options=false, true; display=On` |
| **<** | `c28a54ec-c679-4d09-b086-aa10fbae3b95` | 88 | — |
| **Level Scaler** | `800377c2-1f1c-4804-9440-4c6531047818` | 89 | `LOW (float); value=0.464158883; range=[0, 2]; display=-20.0 dB`<br>`HIGH (float); value=1; range=[0, 2]; display=0.0 dB` |
| **Level** | `0565644e-7e9f-45bf-bc34-8df52b5d7d80` | 90 | `LEVEL (float); value=1; range=[0, 2]; display=0.0 dB` |
| **Lin → dB** | `7091f45b-eb29-41e9-a285-c6173cf52288` | 91 | — |
| **Log** | `1c5671ab-6e13-4b60-90fd-b64142d4004d` | 92 | `BASE (integer); options=0:2, 1:e, 2:10; display=10` |
| **Logic Delay** | `ec697982-2be4-4b87-88d4-333032f18577` | 93 | `DELAY (float); value=-0.921; range=[-4, 1]; display=120 ms`<br>`MODE (integer); options=0:↑, 1:↓, 2:↕; display=↕` |
| **Long Delay** | `f601a44c-8dcb-4ee7-9f2a-ce02ff07948e` | 94 | `UNIT (integer); options=0:Seconds, 1:16th, 2:8th, 3:4th; display=4th`<br>`TIME (float); value=1; range=[0.025, 2]; display=1.00 s`<br>`STEPS (integer); options=0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8; display=8`<br>`OFFSET (float); value=0; range=[-0.5, 0.5]; display=0.00 %` |
| **Low-pass LD** | `85ca7753-049a-419a-bb37-d8c358b10932` | 95 | `CUTOFF (float); value=96; range=[15, 144]; display=2.09 kHz`<br>`RESONANCE (float); value=0.6; range=[0, 1.22]; display=60.0 %`<br>`NONLINEARITY (integer); options=0:Symmetric, 1:Asymmetric; display=Asymmetric`<br>`KEYTRACK (float); value=1; range=[0, 2]; display=100 %`<br>`CUTOFF_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`POLES (integer); options=0:6, 1:12, 2:18, 3:24; display=24`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`Q_LIMIT (float); value=-10; range=[-30, 12]; display=-10.0 dB` |
| **Low-pass MG** | `a72eb152-884e-4bf0-bd22-d21e49fd3466` | 96 | `CUTOFF (float); value=96; range=[15, 144]; display=2.09 kHz`<br>`RESONANCE (float); value=0.6; range=[0, 1.2]; display=60.0 %`<br>`KEYTRACK (float); value=1; range=[0, 2]; display=100 %`<br>`CUTOFF_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`Q_LIMIT (float); value=-10; range=[-30, 12]; display=-10.0 dB` |
| **Low-pass** | `9747205f-2450-42da-89be-200b149b967b` | 97 | `CUTOFF (float); value=102.232645; range=[15, 144]; display=3.00 kHz`<br>`POLES (integer); options=0:1ᴾ, 1:2ᴾ, 2:3ᴾ, 3:4ᴾ, 4:5ᴾ, 5:6ᴾ; display=6ᴾ` |
| **Merge** | `c10b5ffa-0d10-4005-ad49-a39253ee26eb` | 98 | `COUNT (integer); value=2; range=[2, 8]; display=2`<br>`INTERPOLATION (integer); options=0:Nearest, 1:Linear; display=Linear`<br>`WRAP (boolean); value=false; options=false, true; display=Off`<br>`NORMALIZE (boolean); value=true; options=false, true; display=On` |
| **MinMax** | `aaf43587-9228-4bb0-8743-8cbf411e6be7` | 99 | — |
| **Mixer** | `839e96da-cda4-45ce-b5a1-e0a40a176968` | 100 | `PAN_4 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_3 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_2 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_1 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`LEVEL_3 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_2 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_1 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_4 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`ENABLE_1 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_2 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_3 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_4 (boolean); value=true; options=false, true; display=On`<br>`SOLO_1 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_2 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_3 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_4 (boolean); value=false; options=false, true; display=Off`<br>`LEVEL_6 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_5 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`PAN_5 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_6 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`ENABLE_5 (boolean); value=true; options=false, true; display=On`<br>`SOLO_5 (boolean); value=false; options=false, true; display=Off`<br>`ENABLE_6 (boolean); value=true; options=false, true; display=On`<br>`SOLO_6 (boolean); value=false; options=false, true; display=Off` |
| **Mod Delay** | `a8d565fa-fcf5-4ede-bea9-90999f6e8406` | 101 | `TIME (float); value=0.66943295; range=[0, 1.25992105]; display=300 ms`<br>`MODULATION (float); value=0; range=[-1, 0.999]; display=0.00 %`<br>`FEEDBACK (float); value=0; range=[0, 1]; display=0.00 %`<br>`CUTOFF (float); value=144; range=[60, 144]; display=33.5 kHz`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`CLIP_MODE (integer); options=0:Hard, 1:Soft; display=Soft`<br>`UNIT (integer); options=0:Seconds, 1:16th, 2:8th, 3:4th; display=4th`<br>`STEPS (integer); options=0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8; display=8`<br>`OFFSET (float); value=0; range=[-0.5, 0.5]; display=0.00 %` |
| **Modulator Out** | `098ad9c6-b4c9-4ec1-887f-eaf588611056` | 102 | `SOURCE (integer); metadata unavailable` |
| **Multiply** | `4a945068-35ff-469f-bc17-fda5d32b7baa` | 103 | — |
| **N-Latch** | `04685f05-a0bd-4cef-81f8-b59a2e2e16d1` | 104 | `COUNT (integer); value=2; range=[2, 8]; display=2` |
| **NAND** | `328047a0-d0ff-47c6-93ac-44236e228157` | 105 | — |
| **NOR** | `5b278498-4ba5-415b-b159-337edebf952d` | 106 | — |
| **NOT** | `71d887c3-77b6-4ebd-86a9-a23f54a0d606` | 107 | — |
| **Noise** | `33344afa-c8fb-450f-8e82-65fd242a7837` | 108 | `TYPE (integer); options=0:White, 1:Pink; display=Pink`<br>`STEREO (boolean); value=false; options=false, true; display=Off` |
| **≠** | `96507541-21a4-45a0-8bc6-48874e7de89e` | 109 | `EXACT (boolean); value=false; options=false, true; display=Off` |
| **Note In** | `06c1eac9-4d64-4748-8d52-8bf18324d1e7` | 110 | `AFFECT_VOICE_LIFETIME (boolean); value=true; options=false, true; display=On`<br>`SMOOTH (boolean); value=true; options=false, true; display=On`<br>`RELATIVE_TIMBRE (boolean); value=false; options=false, true; display=Off`<br>`ENABLE_EXPRESSIONS (boolean); value=false; options=false, true; display=Off`<br>`ALL_VELOCITIES (boolean); value=true; options=false, true; display=On`<br>`MIDI_CHANNEL (integer); value=0; range=[0, 16]; display=0` |
| **Note Out** | `70baf51d-271c-43c3-b2de-c98fc48f326d` | 111 | `MIDI_CHANNEL (integer); value=1; range=[1, 16]; display=1`<br>`KEY (integer); value=60; range=[0, 127]; display=60`<br>`VELOCITY (float); value=0.8; range=[0, 1]; display=80.0 %`<br>`ENABLE_EXPRESSIONS (boolean); value=true; options=false, true; display=On` |
| **OR** | `3d31b4e4-ce56-4992-a793-39b362f8003a` | 112 | — |
| **Octaver** | `85c173a2-1eb3-4cc1-a19d-84bcb4bde00b` | 113 | `STEREONESS (integer); options=0:Left, 1:Mono, 2:Right; display=Right`<br>`OCTAVE (integer); options=0:-3, 1:-2, 2:-1, 3:0, 4:+1, 5:+2, 6:+3; display=+3` |
| **Oscilloscope** | `0a3b591d-a9b5-44dd-a6ee-a00794df4dc5` | 114 | `MODE (integer); options=0:Slow, 1:Fast, 2:Pitch; display=Pitch`<br>`DISPLAY_MODE (integer); options=0:Last voice, 1:All voices; display=All voices`<br>`Y_BIPOLAR (boolean); value=true; options=false, true; display=On`<br>`Y_RANGE_LIN (float); value=1; range=[1e-06, 100]; display=1.00`<br>`Y_AXIS_MODE (integer); options=0:Linear, 1:Log; display=Log`<br>`RANGE_Y_DB (integer); value=-60; range=[-144, -30]; display=-60`<br>`MAX_Y_DB (integer); value=0; range=[-120, 30]; display=0`<br>`STEREO (boolean); value=false; options=false, true; display=Off` |
| **Pan In** | `3f482022-4a2c-4484-a5d8-d93a1d74e105` | 115 | `SMOOTH (boolean); value=true; options=false, true; display=On` |
| **Pan** | `43600afd-7226-4408-bbb6-b7b9cc2a6cee` | 116 | `PAN (float); value=0; range=[-1, 1]; display=0.00 %` |
| **Ø Bend** | `c2d6358d-9053-49a3-9e1d-9b6c8d0bd539` | 117 | `BEND (float); value=0; range=[-1, 1]; display=0.00 %`<br>`STEREOIZE (boolean); value=false; options=false, true; display=Off` |
| **Ø Counter** | `f9b5157c-0a41-403c-810b-9bbf9a133110` | 118 | `STEPS (integer); value=8; range=[2, 64]; display=8` |
| **Ø Formant** | `9cab8245-ebbf-42ec-ba95-e7bcca4a9cab` | 119 | `SYNC (float); value=0; range=[-48, 48]; display=0.00 st` |
| **Phase In** | `94d89ce0-4a98-4b95-be4a-36814d7b1855` | 120 | — |
| **Ø Lag** | `c03fc75f-c65b-452c-96ea-2ff8de806c26` | 121 | `RATE (float); value=-1.52287875; range=[-6, 1]; display=30.0 ms` |
| **Ø Mirror** | `de0334b8-93bd-463e-824b-dea397e90354` | 122 | `SYNC (float); value=12; range=[0, 48]; display=+12.00 st` |
| **Ø Pinch** | `32323ba6-3a23-4c2d-a2c8-439961ba66ae` | 123 | `BEND (float); value=0; range=[-1, 1]; display=0.00 %`<br>`STEREOIZE (boolean); value=false; options=false, true; display=Off` |
| **Ø Pulse** | `ecab3feb-20ad-494c-9a18-17536832002e` | 124 | `SHARPNESS (float); value=6; range=[0, 6]; display=100 %`<br>`PULSE_WIDTH (float); value=0.5; range=[0, 1]; display=50.0 %` |
| **Ø Reset** | `d04bb748-5f66-4a4a-85d8-d3402c982e22` | 125 | `RETRIGGER (boolean); value=true; options=false, true; display=On` |
| **Ø Reverse** | `89f9e7d1-e36c-446f-937e-a881bf90c7c9` | 126 | `STEREONESS (integer); options=0:Left, 1:Mono, 2:Right; display=Right` |
| **Ø Saw** | `4d7201c8-304a-4b42-95a2-5cc2fa945c18` | 127 | `SHARPNESS (float); value=6; range=[0, 6]; display=100 %` |
| **Ø Scaler** | `53de290f-e7e0-4c71-95d4-dad2c8652691` | 128 | `RATE (float); value=1; range=[0, 32]; display=1.00`<br>`NUMERATOR (integer); value=2; range=[0, 99]; display=2`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1` |
| **Ø Shift** | `727cf275-dd41-4c5a-865d-efee322c04a7` | 129 | `SHIFT (float); value=0; range=[-1, 1]; display=0.00 %`<br>`STEREOIZE (boolean); value=false; options=false, true; display=Off` |
| **Ø Sine** | `2d356600-6e66-49a2-91e5-c14397956a7a` | 130 | — |
| **Ø Sinemod** | `1c248b5d-47ef-401c-94c3-1f4f24d6a88a` | 131 | `AMOUNT (float); value=1.32000612; range=[0, 2]; display=230 %`<br>`RATE (float); value=1; range=[1, 32]; display=1.00`<br>`ADD (boolean); value=true; options=false, true; display=On` |
| **Ø Skew** | `4f2ab665-8fca-4a03-b3b5-f85acdcf393a` | 132 | `SKEW (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`STEREOIZE (boolean); value=false; options=false, true; display=Off` |
| **Ø Split** | `f7272bf8-b86a-491c-b342-8eae1a792da4` | 133 | `N (integer); value=2; range=[2, 8]; display=2`<br>`DIRECTION (integer); options=0:Plus, 1:Minus; display=Minus` |
| **Ø Sync** | `1cd61fc6-74a8-4117-bdb3-54bc8b033f8a` | 134 | `SYNC (float); value=0; range=[0, 48]; display=0.00 st` |
| **Ø Triangle** | `af9a7023-48a9-498e-ab27-33800bcf22f6` | 135 | — |
| **Ø Window** | `7ec54364-46c2-4303-b6c8-66905802f3b3` | 136 | — |
| **Ø Wrap** | `55792b95-b570-4513-b89d-4057c1af338b` | 137 | — |
| **Phase-1** | `44da1c7d-5fef-4d7a-9b1c-739324a59a97` | 138 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`TIMBRE (float); value=0; range=[0, 1]; display=0.00 %`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`FORMANT (integer); value=1; range=[1, 9]; display=1`<br>`ALGORITHM (integer); options=0:SAW, 1:PW, 2:HALF, 3:DBL, 4:SIN; display=SIN`<br>`FEEDBACK (float); value=0; range=[0, 1]; display=0.00 %` |
| **Phaser+** | `50a03b86-dac7-431a-b923-3ab687a54d03` | 139 | `ALTERNATE_MODE (boolean); value=false; options=false, true; display=Off`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`TYPE (integer); options=0:GS, 1:EHx, 2:MX, 3:MF; display=MF`<br>`MIX (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`CURVE (integer); options=0:Phaser, 1:Speaking, 2:Barber ↑, 3:Barber ↓; display=Barber ↓`<br>`CENTER (float); value=0.35; range=[0, 1]; display=35.0 %`<br>`FEEDBACK (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`RATE (float); value=0.5; range=[-2, 1]; display=3.16 Hz`<br>`AMOUNT (float); value=0.5; range=[0, 1]; display=50.0 %` |
| **Phasor** | `2944a921-f9af-4781-9cf7-7fe98218fce3` | 140 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz` |
| **Pinch** | `0df6f770-87b4-45fa-899b-d9e56c253255` | 141 | `BEND (float); value=0; range=[-1, 1]; display=0.00 %`<br>`STEREOIZE (boolean); value=false; options=false, true; display=Off` |
| **Pitch Buss** | `88a039b7-13d3-40c0-9977-bfe37d06c60f` | 142 | `VALUE (float); value=0; range=[-36, 36]; display=0.00 st`<br>`AMOUNT2 (float); value=0; range=[-36, 36]; display=0.00 st`<br>`AMOUNT3 (float); value=0; range=[-36, 36]; display=0.00 st`<br>`AMOUNT4 (float); value=0; range=[-36, 36]; display=0.00 st`<br>`AMOUNT5 (float); value=0; range=[-36, 36]; display=0.00 st`<br>`AMOUNT6 (float); value=0; range=[-36, 36]; display=0.00 st`<br>`THRU2 (boolean); value=false; options=false, true; display=Off`<br>`THRU3 (boolean); value=false; options=false, true; display=Off`<br>`THRU5 (boolean); value=false; options=false, true; display=Off`<br>`THRU4 (boolean); value=false; options=false, true; display=Off`<br>`THRU6 (boolean); value=false; options=false, true; display=Off` |
| **Pitch Class** | `7e371fc4-dae1-426b-8f0b-6dd980e63d31` | 143 | `OCTAVE (integer); options=0:-2, 1:-1, 2:0, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7; display=7`<br>`WRAPPING_KEY (integer); options=0:C, 1:C♯ / D♭, 2:D, 3:D♯ / E♭, 4:E, 5:F, 6:F♯ / G♭, 7:G, 8:G♯ / A♭, 9:A, 10:A♯ / B♭, 11:B; display=B`<br>`KEY (integer); options=0:C, 1:C♯-D♭, 2:D, 3:D♯-E♭, 4:E, 5:F, 6:F♯-G♭, 7:G, 8:G♯-A♭, 9:A, 10:A♯-B♭, 11:B; display=B` |
| **Pitch In** | `b5ce2b79-e881-4105-ad80-4435cc57f75e` | 144 | `NOTE_PRIORITY (integer); options=0:Default, 1:Lowest, 2:Last, 3:Highest; display=Highest` |
| **Pitch Quantize** | `70a58062-9175-4eec-9a25-b8f0f919773b` | 145 | `C (boolean); value=true; options=false, true; display=On`<br>`C# (boolean); value=false; options=false, true; display=Off`<br>`D (boolean); value=false; options=false, true; display=Off`<br>`D# (boolean); value=false; options=false, true; display=Off`<br>`E (boolean); value=false; options=false, true; display=Off`<br>`F (boolean); value=false; options=false, true; display=Off`<br>`G (boolean); value=true; options=false, true; display=On`<br>`A (boolean); value=true; options=false, true; display=On`<br>`B (boolean); value=false; options=false, true; display=Off`<br>`F# (boolean); value=false; options=false, true; display=Off`<br>`G# (boolean); value=false; options=false, true; display=Off`<br>`A# (boolean); value=false; options=false, true; display=Off`<br>`DISTRIBUTION (integer); options=0:Uniform, 1:Nearest (by pitch), 2:Nearest (by octave); display=Nearest (by octave)`<br>`USE_NOTE_INPUT (boolean); value=true; options=false, true; display=On` |
| **Pitch Scaler** | `c53fda13-4ed0-42fd-b410-19052ca6322d` | 146 | `LOW (float); value=0; range=[-120, 120]; display=0.00`<br>`HIGH (float); value=12; range=[-120, 120]; display=12.00` |
| **Pitch Shift** | `69d1a916-2d39-4a4f-9334-7ec4def8eb83` | 147 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`KEYTRACK (boolean); value=false; options=false, true; display=Off`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %`<br>`GRAIN_RATE (float); value=0.74; range=[0.3, 2]; display=5.50 Hz`<br>`MIX (float); value=1; range=[0, 1]; display=100 %`<br>`GRAIN_FADE (float); value=0.05; range=[0.001, 0.3]; display=50.00 ms`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`PMFM (boolean); value=false; options=false, true; display=Off`<br>`ADAPTIVE_GRAIN_RATE (boolean); value=false; options=false, true; display=Off`<br>`GRAIN_PITCH_DENOMINATOR (integer); value=48; range=[1, 99]; display=1:48` |
| **Pitch → Freq** | `4ef26e44-92c8-42f0-a4fd-b70b3a3769cb` | 148 | `UNIT (integer); options=0:Hertz, 1:Kilohertz; display=Kilohertz`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz` |
| **Pitch → Ø** | `f31bdee3-3f0c-4861-9a93-7514401a8a6f` | 149 | — |
| **Pitch** | `9adcd4b7-5dab-43cc-82da-ec5873ac3c72` | 150 | `STEREOIZE (boolean); value=false; options=false, true; display=Off`<br>`VALUE (float); value=0; range=[-128, 128]; display=0.00`<br>`LEARN (boolean); options=false, true` |
| **Pitches** | `c9b6cefc-c467-45b6-aedb-ba02a9f887fe` | 151 | `STEPS (integer); value=8; range=[2, 64]; display=8`<br>`SCROLL_Y (integer); value=0; range=[-9, 9]; display=0`<br>`ZOOM_Y (integer); value=1; range=[1, 4]; display=±1`<br>`DEVICE_PHASE (boolean); value=true; options=false, true; display=On`<br>`MUTE_WHEN_STOPPED (boolean); value=false; options=false, true; display=Off`<br>`NUDGE_RIGHT (boolean); options=false, true`<br>`NUDGE_UP (boolean); options=false, true`<br>`NUDGE_LEFT (boolean); options=false, true`<br>`SET_ALL (boolean); options=false, true`<br>`NUDGE_DOWN (boolean); options=false, true`<br>`RESET_NOTE (integer); value=60; range=[0, 127]; display=60` |
| **Pluck** | `0ae4fef0-e859-4085-a100-448f5158eafb` | 152 | `ATTACK (float); value=0.221714286; range=[0, 0.5]; display=10.9 ms`<br>`DECAY (float); value=0.794; range=[0, 3]; display=501 ms`<br>`ENVELOPE (integer); metadata unavailable`<br>`GATE (boolean); value=true; options=false, true; display=On`<br>`AFFECT_VOICE_LIFETIME (boolean); value=true; options=false, true; display=On`<br>`RELEASE (float); value=0.625101714; range=[0, 3]; display=244 ms` |
| **Poly → Mono** | `0309fc67-0290-42b8-8ea3-625b333cb34c` | 153 | `MODE (integer); options=0:Last, 1:Sum, 2:Average, 3:Min, 4:Max; display=Max` |
| **Power** | `6808a887-6a5a-465d-ab48-84fb0995d2ca` | 154 | — |
| **Pressure In** | `2f6804b9-87a8-4c06-a61b-31e4171e1f2d` | 155 | `SMOOTH (boolean); value=true; options=false, true; display=On` |
| **Probabilities** | `a65c43a5-f59a-460a-b22f-88571ac380ec` | 156 | `STEPS (integer); value=8; range=[2, 64]; display=8`<br>`DEVICE_PHASE (boolean); value=true; options=false, true; display=On`<br>`MUTE_WHEN_STOPPED (boolean); value=false; options=false, true; display=Off`<br>`RANDOM_TRIGGER (boolean); options=false, true`<br>`CLEAR_TRIGGER (boolean); options=false, true`<br>`FILL_TRIGGER (boolean); options=false, true`<br>`NUDGE_LEFT (boolean); options=false, true`<br>`NUDGE_RIGHT (boolean); options=false, true` |
| **Product** | `93e8af3d-0cb4-41e4-b9cb-dc825b5fc5d7` | 157 | — |
| **Pulse** | `10c3be1f-ceb4-4bbc-bf35-af11285e58e0` | 158 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`TIMBRE (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`WRAP (float); value=0; range=[0, 48]; display=0.00 st`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`BIPOLAR (boolean); value=true; options=false, true; display=On` |
| **Push** | `b7573eb6-2902-4f89-98cf-2c33b9f1b43b` | 159 | `DRIVE (float); value=0; range=[0, 40]; display=0.0 dB`<br>`AA (boolean); value=true; options=false, true; display=On` |
| **Quantize** | `c1f45a63-edde-4c38-b588-efbd4c1e35ec` | 160 | — |
| **Quantizer** | `00e05a87-8b61-4540-9746-d8298406bc5a` | 161 | `STEP_SIZE (float); value=-12; range=[-60, 0]; display=-12.0 dB`<br>`AA (boolean); value=true; options=false, true; display=On` |
| **Rasp** | `3a06f9a2-b1ec-42ff-bb55-35b42fcff581` | 162 | `CUTOFF (float); value=95.9751302; range=[15, 144]; display=2.09 kHz`<br>`RESONANCE (float); value=0.45; range=[0, 1]; display=45.0 %`<br>`KEYTRACK (float); value=1; range=[0, 2]; display=100 %`<br>`CUTOFF_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`FB_LIMIT (float); value=0.9; range=[0.35, 1]; display=90.0 %`<br>`BEND_AMOUNT (float); value=0; range=[-1, 1]; display=0.00 %`<br>`BEND_MODE (integer); options=0:Shift, 1:Double, 2:Gravity; display=Gravity`<br>`FILTER_TYPE (integer); options=0:Low-pass, 1:Band-pass; display=Band-pass` |
| **Ratio** | `7ab5e7c4-671e-40de-8c06-21dd273c908c` | 163 | `DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[1, 99]; display=1`<br>`STEREONESS (integer); options=0:Left, 1:Mono, 2:Right; display=Right` |
| **Reciprocal** | `f4f35d7b-5fdd-40bd-98d8-c142e5ca66a8` | 164 | `STEREONESS (integer); options=0:Left, 1:Mono, 2:Right; display=Right`<br>`INVERT (boolean); value=true; options=false, true; display=On` |
| **Recorder** | `bdedc713-81ba-40b5-878c-a2e979ec2393` | 165 | — |
| **Rectifier** | `ac6de5ed-c143-4364-9989-3c7d299db380` | 166 | `POSITIVE (float); value=1; range=[-1, 1]; display=100 %`<br>`NEGATIVE (float); value=0; range=[-1, 1]; display=0.00 %`<br>`AA (boolean); value=true; options=false, true; display=On` |
| **Ripple** | `0b4317c5-7880-4515-ab71-b4607ddc8fdb` | 167 | `CUTOFF2 (float); value=84; range=[15, 144]; display=1.05 kHz`<br>`KEYTRACK (float); value=1; range=[0, 2]; display=100 %`<br>`CUTOFF_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`CUTOFF (float); value=96; range=[15, 144]; display=2.09 kHz`<br>`FBK_GAIN (float); value=0.25; range=[-1, 1]; display=25.0 %`<br>`COLOR_MODE (integer); options=0:Earth, 1:Wind, 2:Fire; display=Fire`<br>`FWD_HARD (boolean); value=false; options=false, true; display=Off`<br>`FBK_HARD (boolean); value=false; options=false, true; display=Off`<br>`LOW_QUALITY (boolean); value=false; options=false, true; display=Off` |
| **Root Key** | `1bc70e1f-5d9d-407e-a087-e222ef63089e` | 168 | `OCTAVE (integer); options=0:-2, 1:-1, 2:0, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7; display=7`<br>`WRAPPING_KEY (integer); options=0:C, 1:C♯ / D♭, 2:D, 3:D♯ / E♭, 4:E, 5:F, 6:F♯ / G♭, 7:G, 8:G♯ / A♭, 9:A, 10:A♯ / B♭, 11:B; display=B` |
| **Roots** | `28166c20-3a55-45e8-8117-bfec9a62a4d4` | 169 | `DEGREE (integer); value=2; range=[1, 9]; display=2` |
| **Round** | `ae80ebb6-e84f-4cc9-848e-1dee19db8181` | 170 | — |
| **S/H LFO** | `965f7fc4-3f76-4e83-8870-98673cb0576a` | 171 | `RATE_MOD (float); value=0; range=[-32, 32]; display=0.00`<br>`RETRIGGER (boolean); value=true; options=false, true; display=On`<br>`BIPOLAR (boolean); value=false; options=false, true; display=Off`<br>`TIMEBASE (integer); options=0:Hertz, 1:Kilohertz, 2:Bar, 3:Half note, 4:Quarter note, 5:8th note, 6:16th note, 7:32nd note, 8:Dotted half note, 9:Dotted quarter note, 10:Dotted 8th note, 11:Dotted 16th note, 12:Dotted 32nd note, 13:Triplet half note, 14:Triplet quarter note, 15:Triplet 8th note, 16:Triplet 16th note, 17:Triplet 32nd note, 18:Hold; display=Hold`<br>`RATE (float); value=1; range=[0, 32]; display=1.00`<br>`PHASE (float); value=0; range=[-360, 360]; display=0 °`<br>`LFO (integer); metadata unavailable`<br>`PHASE_MOD (float); value=0; range=[0, 1]; display=0.00`<br>`FEEDBACK (float); value=0; range=[-1, 1]; display=0.00 %`<br>`SMOOTH (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`RPHASE (float); value=0; range=[-360, 360]; display=0 °`<br>`FEEDBACK_LENGTH (integer); value=1; range=[1, 32]; display=N = 1` |
| **SVF** | `2ddd3d4f-04b9-4ad5-a6f7-08e01df14c0f` | 172 | `CUTOFF (float); value=96; range=[15, 144]; display=2.09 kHz`<br>`RESONANCE (float); value=0.6; range=[0, 2]; display=60.0 %`<br>`KEYTRACK (float); value=1; range=[0, 2]; display=100 %`<br>`CUTOFF_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`TYPE (integer); options=0:Low-pass, 1:Band-pass, 2:High-pass, 3:Notch; display=Notch`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`Q_LIMIT (float); value=-10; range=[-30, 16]; display=-10.0 dB` |
| **Sallen-Key** | `726cd882-3d94-4140-b2b7-cfa7f416cc69` | 173 | `CUTOFF (float); value=96; range=[15, 144]; display=2.09 kHz`<br>`RESONANCE (float); value=0.0702; range=[0, 1.22]; display=7.02 %`<br>`NONLINEARITY (integer); options=0:Symmetric, 1:Asymmetric; display=Asymmetric`<br>`KEYTRACK (float); value=1; range=[0, 2]; display=100 %`<br>`CUTOFF_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`POLES (integer); options=0:LP 1ᴾ, 1:LP 2ᴾ, 2:LP 3ᴾ, 3:LP 4ᴾ, 4:LP 6ᴾ, 5:LP 8ᴾ, 6:BP 2ᴾ, 7:BP 4ᴾ, 8:BP 6ᴾ, 9:BP 8ᴾ, 10:HP 1ᴾ, 11:HP 2ᴾ, 12:HP 3ᴾ, 13:HP 4ᴾ, 14:HP 6ᴾ, 15:HP 8ᴾ; display=HP 8ᴾ`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`Q_LIMIT (float); value=-10; range=[-30, 12]; display=-10.0 dB` |
| **Sample / Hold** | `8214fd6c-5131-49d2-a9a6-709760a46b82` | 174 | — |
| **Sampler** | `40c0fe10-37ae-4d05-9ce1-d0bac5cd2b8e` | 175 | `SAMPLE_START (float); value=0; range=[0, 1]; display=0.00 %`<br>`LOOP_START (float); value=0; range=[0, 1]; display=0.00 %`<br>`LOOP_LENGTH (float); value=1; range=[0, 1]; display=100 %`<br>`PITCH (float); value=0; range=[-36, 36]; display=0.00 st`<br>`SAMPLE (boolean); options=false, true`<br>`RETRIGGER (boolean); value=true; options=false, true; display=On`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`USE_VELOCITY (boolean); value=true; options=false, true; display=On`<br>`FORMANT (float); value=0; range=[-24, 24]; display=0.00 st`<br>`GRAIN_SIZE (float); value=-1.52287875; range=[-3, -0.522878745]; display=30.0 ms`<br>`SPEED (float); value=1; range=[-4, 4]; display=100 %`<br>`FREEZE_PLAYHEAD (boolean); value=false; options=false, true; display=Off`<br>`PLAY_MODE (integer); options=0:Repitch, 1:Cycles, 2:Textures; display=Textures`<br>`SELECT (float); value=0; range=[0, 1]; display=0.0`<br>`PLAYHEAD_MOTION (float); value=0; range=[0, 2]; display=0.00 %` |
| **Saturator** | `267e71c5-6aad-41f6-92da-3127e3bd1a25` | 176 | `KNEE_SKEW (float); value=0; range=[-1, 1]; display=0.00 %`<br>`HIGH_RATIO (float); value=-1; range=[-2, 0]; display=-100 %`<br>`NORMALIZE (boolean); value=true; options=false, true; display=On`<br>`LOW_KNEE (float); value=6.2; range=[0, 24]; display=+6.2 dB`<br>`HIGH_THRESHOLD (float); value=-8.05; range=[-40, 0]; display=-8.0 dB`<br>`SKEW_THRESHOLD (float); value=5.88; range=[-12, 12]; display=5.88`<br>`RATIO_SKEW (float); value=0; range=[-1, 1]; display=0.00 %`<br>`HIGH_KNEE (float); value=-6; range=[-24, 0]; display=-6.0 dB`<br>`LOW_RATIO (float); value=0; range=[-4, 1]; display=0.00 %`<br>`LOW_THRESHOLD (float); value=-30; range=[-40, 0]; display=-30.0 dB`<br>`DRIVE (float); value=1; range=[0, 3]; display=0.0 dB`<br>`CUTOFF (float); value=83.213; range=[15, 144]; display=1.00 kHz`<br>`POLES (integer); options=0:Off, 1:1ᴳ, 2:1ᴿ, 3:2ᴳ, 4:2ᴿ, 5:3ᴳ, 6:3ᴿ, 7:4ᴳ, 8:4ᴿ, 9:5ᴳ, 10:5ᴿ, 11:6ᴳ, 12:6ᴿ; display=6ᴿ`<br>`OUTPUT (float); value=0; range=[-12, 12]; display=0.0 dB` |
| **Sawtooth** | `4ae6d37a-5412-4691-aa8b-261e94e60c59` | 177 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`TIMBRE (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`WRAP (float); value=0; range=[0, 48]; display=0.00 st`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`BIPOLAR (boolean); value=true; options=false, true; display=On` |
| **Scale Steps** | `0015d740-8c68-4576-834e-2d4dabef24e1` | 178 | `STEREONESS (integer); options=0:Left, 1:Mono, 2:Right; display=Right`<br>`STEPS (integer); value=0; range=[-32, 32]; display=0`<br>`CONSTRAIN_MODE (integer); options=0:Quantize Up, 1:Smart Constrain, 2:Quantize Down; display=Quantize Down` |
| **Scrawl** | `9c1aa872-f271-4bd6-9f0d-37157399569c` | 179 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`CURVE (boolean); options=false, true`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %` |
| **Segments** | `953b71a0-c496-4cdc-8d50-843373d248b5` | 180 | `ENVELOPE (integer); metadata unavailable`<br>`CURVE (boolean); options=false, true`<br>`GATE (boolean); value=true; options=false, true; display=On`<br>`RATE (float); value=0; range=[-1.7, 1.699]; display=1.00`<br>`TIMEBASE (integer); options=0:Minutes, 1:Seconds, 2:Milliseconds, 3:Bar, 4:Half note, 5:Quarter note, 6:8th note, 7:16th note, 8:32nd note, 9:Dotted half note, 10:Dotted quarter note, 11:Dotted 8th note, 12:Dotted 16th note, 13:Dotted 32nd note, 14:Triplet half note, 15:Triplet quarter note, 16:Triplet 8th note, 17:Triplet 16th note, 18:Triplet 32nd note, 19:Hold (rate of zero); display=Hold (rate of zero)`<br>`AFFECT_VOICE_LIFETIME (boolean); value=true; options=false, true; display=On`<br>`ENABLE_SMOOTH (boolean); value=true; options=false, true; display=On`<br>`TIME (float); value=-2; range=[-5, 1]; display=10.0 ms` |
| **Select In** | `c6923eb3-e161-4eed-8a93-a4554287a77b` | 181 | — |
| **Select Out** | `4228f753-5073-4aa4-81c1-ec7f65b2ca23` | 182 | — |
| **Shift Register** | `749fc1c8-9f66-43bb-b11d-fbd7e5e84c02` | 183 | `COUNT (integer); value=2; range=[2, 8]; display=2` |
| **Shred** | `cd8d3ec5-9655-4f5f-9a45-5aaf87edaa57` | 184 | `DRIVE (float); value=0; range=[0, 40]; display=0.0 dB`<br>`AA (boolean); value=true; options=false, true; display=On` |
| **Sine** | `ca05aebd-ecaf-4d57-b0f6-c04ce81674c4` | 185 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`TIMBRE (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`WRAP (float); value=0; range=[0, 48]; display=0.00 st`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`BIPOLAR (boolean); value=true; options=false, true; display=On` |
| **Slope ↗** | `4da936f3-c96b-43f6-b716-6a70407a38fc` | 186 | `TIME (float); value=-2.825; range=[-4, 1]; display=1.50 ms` |
| **Slope ↘** | `78e296cf-9ac8-415a-96c3-b7e924e061f3` | 187 | `TIME (float); value=-1; range=[-4, 1]; display=100 ms` |
| **Slopes** | `0b754e8c-cfb6-4399-aabe-c23d7e635f72` | 188 | `SOURCE (integer); metadata unavailable`<br>`DEVICE_PHASE (boolean); value=true; options=false, true; display=On`<br>`MUTE_WHEN_STOPPED (boolean); value=false; options=false, true; display=Off`<br>`CURVE (boolean); options=false, true` |
| **Soar** | `d7ca54e4-1d83-4dec-a40e-14d40fbd5ab5` | 189 | `DRIVE (float); value=0; range=[0, 40]; display=0.0 dB`<br>`AA (boolean); value=true; options=false, true; display=On` |
| **Spectrum** | `9fe38e12-614b-470c-9dde-789fbde43f30` | 190 | `TILT (integer); options=0:0 dB/oct, 1:1.5 dB/oct, 2:3 dB/oct, 3:4.5 dB/oct, 4:6 dB/oct; display=6 dB/oct`<br>`STYLE_1 (integer); options=0:Lines, 1:Dots, 2:Bins, 3:Fill; display=Fill`<br>`STYLE_2 (integer); options=0:Lines, 1:Dots, 2:Bins, 3:Fill; display=Fill`<br>`STYLE_3 (integer); options=0:Lines, 1:Dots, 2:Bins, 3:Fill; display=Fill`<br>`STYLE_4 (integer); options=0:Lines, 1:Dots, 2:Bins, 3:Fill; display=Fill`<br>`SCALE_X (integer); options=0:Lin, 1:Log; display=Log`<br>`RANGE_Y (integer); value=-120; range=[-144, -30]; display=-120`<br>`MAX_Y (integer); value=0; range=[-120, 30]; display=0` |
| **Split** | `61968cb5-c43f-41ce-bbb9-07e649dc38a5` | 191 | `COUNT (integer); value=2; range=[2, 8]; display=2`<br>`INTERPOLATION (integer); options=0:Nearest, 1:Linear; display=Linear`<br>`WRAP (boolean); value=false; options=false, true; display=Off`<br>`NORMALIZE (boolean); value=true; options=false, true; display=On` |
| **Step Access** | `c74b57ac-0295-4daf-979a-b6248efbde7c` | 192 | `SHUFFLE (boolean); value=false; options=false, true; display=Off`<br>`LENGTH (integer); value=4; range=[1, 64]; display=4`<br>`OFFSET (integer); value=0; range=[-64, 64]; display=0`<br>`FREERUN (boolean); value=false; options=false, true; display=Off`<br>`TIMEBASE (integer); options=0:Bar, 1:Half note, 2:Quarter note, 3:8th note, 4:16th note, 5:32nd note, 6:Dotted half note, 7:Dotted quarter note, 8:Dotted 8th note, 9:Dotted 16th note, 10:Dotted 32nd note, 11:Triplet half note, 12:Triplet quarter note, 13:Triplet 8th note, 14:Triplet 16th note, 15:Triplet 32nd note; display=Triplet 32nd note`<br>`RANGE (integer); value=8; range=[1, 64]; display=8` |
| **Steps** | `80d4de64-0ebc-4bb8-b448-74e57240f4a9` | 193 | `STEPS (integer); value=8; range=[2, 64]; display=8`<br>`BIPOLAR (boolean); value=false; options=false, true; display=Off`<br>`SOURCE (integer); metadata unavailable`<br>`DEVICE_PHASE (boolean); value=true; options=false, true; display=On`<br>`INTERPOLATION (boolean); value=false; options=false, true; display=Off`<br>`MUTE_WHEN_STOPPED (boolean); value=false; options=false, true; display=Off`<br>`CLEAR_TRIGGER (boolean); options=false, true`<br>`RANDOM_TRIGGER (boolean); options=false, true`<br>`NUDGE_LEFT (boolean); options=false, true`<br>`NUDGE_RIGHT (boolean); options=false, true` |
| **Stereo Merge** | `36096881-77f5-4ce1-b8c5-b3b21e6440f3` | 194 | — |
| **Stereo Split** | `842ae87e-de89-4583-9f24-43b91a218d1f` | 195 | — |
| **Stereo Width** | `a34edcba-25b3-4f07-86b2-81701b092d66` | 196 | `WIDTH (float); value=1; range=[0, 2]; display=100 %` |
| **Sub** | `d1263096-fddf-438f-9c9f-ed9c1693e954` | 197 | `KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`WAVEFORM (integer); options=0:Sine, 1:Half-sine, 2:Triangle, 3:Pulse 50%, 4:Pulse 25%, 5:Sawtooth; display=Sawtooth`<br>`OCTAVE (integer); options=0:0, 1:-1, 2:-2; display=-2`<br>`INVERT (boolean); value=false; options=false, true; display=Off`<br>`BIPOLAR (boolean); value=true; options=false, true; display=On` |
| **Subtract** | `1c779472-00d1-459c-9532-6b01d3baab1a` | 198 | — |
| **Sum** | `5b414321-7adb-4210-ab26-d2367a8b5d56` | 199 | — |
| **Swarm** | `faea6af4-72db-42c6-adac-0f74d8ebdbbf` | 200 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`SPREAD (float); value=0.5; range=[0, 1]; display=0.13`<br>`SKIRT (float); value=0; range=[-1, 1]; display=0.00 %`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`WAVEFORM (integer); options=0:Saw, 1:Sine; display=Sine` |
| **Timbre In** | `21a6a402-2611-4311-b372-f36d36ad25d8` | 201 | `SMOOTH (boolean); value=true; options=false, true; display=On`<br>`RELATIVE_TIMBRE (boolean); value=false; options=false, true; display=Off` |
| **Toggle In** | `168a4502-2ec0-4222-b6cb-5a01875bc543` | 202 | `VALUE (boolean); value=false; options=false, true; display=Off` |
| **Toggle Out** | `f75deac4-c3d0-4630-a09c-4bbdac03c9d3` | 203 | `VALUE (boolean); value=false; options=false, true; display=Off` |
| **Toggle** | `5d016b16-be9c-4735-b9df-a533ee72528b` | 204 | `VALUE (boolean); value=true; options=false, true; display=On` |
| **Transfer** | `3b18c07d-c4cb-4195-9c85-6b37ca1c048a` | 205 | `CURVE (boolean); options=false, true`<br>`DRIVE (float); value=0; range=[-24, 24]; display=0.0 dB` |
| **Transport Playing** | `9714df20-f4ea-4017-a874-4ccb554dd86e` | 206 | — |
| **Transport** | `997869ea-e649-4ac8-865e-bd4ac9e7b2a2` | 207 | `SHUFFLE (boolean); value=false; options=false, true; display=Off`<br>`LENGTH (integer); value=16; range=[1, 99]; display=16`<br>`OFFSET (integer); value=0; range=[-16, 16]; display=0`<br>`TIMEBASE (integer); options=0:bar, 1:2nd, 2:4th, 3:8th, 4:16th, 5:32nd; display=32nd`<br>`FREERUN (boolean); value=true; options=false, true; display=On` |
| **Transpose** | `35de4fbc-95f6-4719-911a-bc81a2d48df4` | 208 | `VALUE (float); value=0; range=[-36, 36]; display=0.00 st`<br>`STEREONESS (integer); options=0:Left, 1:Mono, 2:Right; display=Right` |
| **Triangle** | `9ab5d37c-f1ae-47a0-b85d-0f5b7c4fdb90` | 209 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`TIMBRE (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`WRAP (float); value=0; range=[0, 48]; display=0.00 st`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`BIPOLAR (boolean); value=true; options=false, true; display=On` |
| **Trigger** | `d6aa9f53-8cc6-45a5-8fc7-f4ba97274b77` | 210 | `TRIGGER (boolean); options=false, true` |
| **Triggers** | `e75916a0-2594-4181-88a4-b19fdb77c0eb` | 211 | `STEPS (integer); value=4; range=[1, 64]; display=4`<br>`DEVICE_PHASE (boolean); value=true; options=false, true; display=On`<br>`MUTE_WHEN_STOPPED (boolean); value=false; options=false, true; display=Off` |
| **Uni → Bi** | `9d4c07ec-ea76-4c30-8c4e-ab94a192ec43` | 212 | — |
| **Union** | `df0a08cc-68b4-4fb2-a662-05cb09745e37` | 0 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`SAW (float); value=1; range=[0, 1]; display=100 %`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`TRI (float); value=0; range=[0, 1]; display=0.00 %`<br>`PULSE (float); value=0; range=[0, 1]; display=0.00 %`<br>`PW (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`BIPOLAR (boolean); value=true; options=false, true; display=On` |
| **VU Meter** | `08d55d78-9240-43b9-9fe3-acde57ac1e60` | 214 | — |
| **Value Readout** | `8ac47e6d-1f50-41c0-91d1-0e4fa33e2f52` | 215 | `MODE (integer); options=0:1, 1:dB, 2:st, 3:Hz; display=Hz`<br>`DISPLAY_MODE (integer); options=0:Last voice, 1:All voices; display=All voices` |
| **Value Scaler** | `512afe2b-0065-46b2-a65f-c8524b9e3552` | 216 | `LOW (boolean); value=-0.5; options=false, true; display=-50.0 %`<br>`HIGH (boolean); value=0.5; options=false, true; display=50.0 %` |
| **Value** | `1faa5baf-6cdf-406a-b0e4-89b67501d982` | 217 | `VALUE (boolean); value=0; options=false, true; display=0.00 %`<br>`STEREOIZE (boolean); value=false; options=false, true; display=Off` |
| **Velo Mult** | `e74a80e4-9c17-49a8-9e84-98d07d6187bb` | 218 | `DEPTH (float); value=0.5; range=[0, 1]; display=50.0 %`<br>`TIME (float); value=-3.02; range=[-5, 0]; display=0.95 ms`<br>`RESPONSE (integer); options=0:Linear, 1:Perceptual; display=Perceptual` |
| **Velocity In** | `1ab8dfab-0671-406c-a423-5f362f5a62ca` | 219 | `VELOCITY_MODE (integer); options=0:Note Ons, 1:Note Offs, 2:Ons & Offs; display=Ons & Offs` |
| **Voice Stack Info** | `7a8675a4-be5a-4393-9257-c10b25358bfa` | 220 | `NORMALIZE (boolean); value=true; options=false, true; display=On` |
| **Voice Stack Mix** | `d58ced40-e61d-4988-8321-3a3456cdfe15` | 221 | `PAN_4 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_3 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_2 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_1 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`LEVEL_3 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_2 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_1 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_4 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`ENABLE_1 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_2 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_3 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_4 (boolean); value=true; options=false, true; display=On`<br>`SOLO_1 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_2 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_3 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_4 (boolean); value=false; options=false, true; display=Off`<br>`LEVEL_6 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_5 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`PAN_5 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_6 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`ENABLE_5 (boolean); value=true; options=false, true; display=On`<br>`SOLO_5 (boolean); value=false; options=false, true; display=Off`<br>`ENABLE_6 (boolean); value=true; options=false, true; display=On`<br>`SOLO_6 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_12 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_10 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_11 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_9 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_8 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_7 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_15 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_16 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_14 (boolean); value=false; options=false, true; display=Off`<br>`SOLO_13 (boolean); value=false; options=false, true; display=Off`<br>`PAN_12 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_11 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_10 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_9 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_8 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_7 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_14 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_15 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_16 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`PAN_13 (float); value=0; range=[-1, 1]; display=0.00 %`<br>`ENABLE_12 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_11 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_9 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_10 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_8 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_7 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_15 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_16 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_14 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_13 (boolean); value=true; options=false, true; display=On`<br>`LEVEL_9 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_8 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_10 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_11 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_12 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_7 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_14 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_13 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_15 (float); value=1; range=[0, 1.259]; display=0.0 dB`<br>`LEVEL_16 (float); value=1; range=[0, 1.259]; display=0.0 dB` |
| **Voice Stack Tog** | `b96d7a4a-d0c8-4d4e-b069-98908e1fa2ea` | 222 | `ENABLE_1 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_2 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_3 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_4 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_5 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_6 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_12 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_11 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_9 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_10 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_8 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_7 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_15 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_16 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_14 (boolean); value=true; options=false, true; display=On`<br>`ENABLE_13 (boolean); value=true; options=false, true; display=On` |
| **Vowels** | `b4c661b9-576e-46ac-8be2-4974dd2f40ce` | 223 | `PITCH_OFFSET (float); value=0; range=[-48, 48]; display=0.00 st`<br>`RESONANCE (float); value=0; range=[-1, 1]; display=100 %`<br>`VOWEL_MOD (float); value=0; range=[-1, 1]; display=0.00 %`<br>`CUTOFF_MOD (float); value=0; range=[-1, 1]; display=0.00 %`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`Q_LIMIT (float); value=-10; range=[-30, 16]; display=-10.0 dB`<br>`VOWEL (float); value=0; range=[-1, 1]; display=0.00 %`<br>`VOWEL_1 (integer); options=0:i, 1:y, 2:ɪ, 3:ʏ, 4:ɨ, 5:ʉ, 6:ɯ, 7:u, 8:e, 9:ø, 10:ɘ, 11:ɵ, 12:ɣ, 13:o, 14:ə, 15:ɛ, 16:œ, 17:ɜ, 18:ɞ, 19:ʌ, 20:ɔ, 21:æ, 22:ɐ, 23:a, 24:Œ, 25:ɑ, 26:ɒ; display=ɒ`<br>`VOWEL_2 (integer); options=0:–, 1:i, 2:y, 3:ɪ, 4:ʏ, 5:ɨ, 6:ʉ, 7:ɯ, 8:u, 9:e, 10:ø, 11:ɘ, 12:ɵ, 13:ɣ, 14:o, 15:ə, 16:ɛ, 17:œ, 18:ɜ, 19:ɞ, 20:ʌ, 21:ɔ, 22:æ, 23:ɐ, 24:a, 25:Œ, 26:ɑ, 27:ɒ; display=ɣ`<br>`VOWEL_3 (integer); options=0:i, 1:y, 2:ɪ, 3:ʏ, 4:ɨ, 5:ʉ, 6:ɯ, 7:u, 8:e, 9:ø, 10:ɘ, 11:ɵ, 12:ɣ, 13:o, 14:ə, 15:ɛ, 16:œ, 17:ɜ, 18:ɞ, 19:ʌ, 20:ɔ, 21:æ, 22:ɐ, 23:a, 24:Œ, 25:ɑ, 26:ɒ; display=o`<br>`VOWEL_4 (integer); options=0:–, 1:i, 2:y, 3:ɪ, 4:ʏ, 5:ɨ, 6:ʉ, 7:ɯ, 8:u, 9:e, 10:ø, 11:ɘ, 12:ɵ, 13:ɣ, 14:o, 15:ə, 16:ɛ, 17:œ, 18:ɜ, 19:ɞ, 20:ʌ, 21:ɔ, 22:æ, 23:ɐ, 24:a, 25:Œ, 26:ɑ, 27:ɒ; display=ɣ`<br>`VOWEL_5 (integer); options=0:i, 1:y, 2:ɪ, 3:ʏ, 4:ɨ, 5:ʉ, 6:ɯ, 7:u, 8:e, 9:ø, 10:ɘ, 11:ɵ, 12:ɣ, 13:o, 14:ə, 15:ɛ, 16:œ, 17:ɜ, 18:ɞ, 19:ʌ, 20:ɔ, 21:æ, 22:ɐ, 23:a, 24:Œ, 25:ɑ, 26:ɒ; display=ɐ`<br>`FREQ_SHIFT (float); value=0; range=[-500, 500]; display=0.00 Hz`<br>`PROFILE (integer); options=0:Women 1, 1:Women 2, 2:Female, 3:Men 1, 4:Men 2, 5:Male, 6:Kids; display=Kids`<br>`TOPOLOGY (integer); options=0:Cascade, 1:LP/BP, 2:LP/BP/HP; display=LP/BP/HP`<br>`KEYTRACK (float); value=1; range=[0, 2]; display=100 %` |
| **Wavefolder** | `aef23bda-40b6-4dba-86f5-044f617574e4` | 224 | `DRIVE (float); value=0; range=[0, 40]; display=0.0 dB`<br>`AA (boolean); value=true; options=false, true; display=On` |
| **Wavetable LFO** | `d2524378-5019-40e7-af9f-08ec6aafce7e` | 225 | `RATE_MOD (float); value=0; range=[-32, 32]; display=0.00`<br>`RETRIGGER (boolean); value=true; options=false, true; display=On`<br>`BIPOLAR (boolean); value=false; options=false, true; display=Off`<br>`TIMEBASE (integer); options=0:Hertz, 1:Kilohertz, 2:Bar, 3:Half note, 4:Quarter note, 5:8th note, 6:16th note, 7:32nd note, 8:Dotted half note, 9:Dotted quarter note, 10:Dotted 8th note, 11:Dotted 16th note, 12:Dotted 32nd note, 13:Triplet half note, 14:Triplet quarter note, 15:Triplet 8th note, 16:Triplet 16th note, 17:Triplet 32nd note, 18:Hold; display=Triplet 8th note`<br>`RATE (float); value=1; range=[0, 32]; display=1.00`<br>`PHASE (float); value=0; range=[-360, 360]; display=0 °`<br>`LFO (integer); metadata unavailable`<br>`PHASE_MOD (float); value=0; range=[0, 1]; display=0.00 %`<br>`RPHASE (float); value=0; range=[-360, 360]; display=0 °`<br>`TABLE_INDEX (float); value=0; range=[0, 1]; display=0.00 %`<br>`TABLE_MOD (float); value=0; range=[-1, 1]; display=0.00 %`<br>`LATCH_INDEX (boolean); value=false; options=false, true; display=Off`<br>`TRANSPORT_SYNC (boolean); value=false; options=false, true; display=Off` |
| **Wavetable** | `19749bf6-0974-4356-9bce-6ab3b5a1af04` | 226 | `PITCH (float); value=0; range=[-48, 48]; display=0.00 st`<br>`TABLE_INDEX (float); value=0; range=[0, 1]; display=0.00 %`<br>`KEYTRACK (boolean); value=true; options=false, true; display=On`<br>`PITCH_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`PHASE_MOD (float); value=0; range=[0, 2]; display=0.00 %`<br>`STEREO (boolean); value=false; options=false, true; display=Off`<br>`RETRIGGER (boolean); value=false; options=false, true; display=Off`<br>`DETUNE (float); value=0; range=[-3, 3]; display=0.00 Hz`<br>`DENOMINATOR (integer); value=1; range=[1, 99]; display=1`<br>`NUMERATOR (integer); value=1; range=[0, 99]; display=1`<br>`WAVETABLE (boolean); options=false, true`<br>`TABLE_MOD (float); value=0; range=[-1, 1]; display=0.00 %`<br>`UNISON_DETUNE (float); value=0.2; range=[0, 1]; display=20 cents`<br>`UNISON_SPREAD (float); value=1; range=[0, 1]; display=100 %`<br>`UNISON (integer); options=0:Off, 1:3, 2:5, 3:7, 4:16; display=16` |
| **XNOR** | `c533df98-a287-4bdb-b1d9-1a694470721b` | 227 | — |
| **XOR** | `e6254ddf-6ba9-47f5-a6ac-402e2fc29a6c` | 228 | — |
| **XP** | `6cccc56b-cd93-435d-bae0-4d10c35c387a` | 229 | `CUTOFF (float); value=96; range=[15, 144]; display=2.09 kHz`<br>`RESONANCE (float); value=0.6; range=[0, 1.22]; display=60.0 %`<br>`KEYTRACK (float); value=1; range=[0, 2]; display=100 %`<br>`CUTOFF_MOD (float); value=0; range=[-1, 1]; display=0.00 st`<br>`DRIVE (float); value=1; range=[0, 2]; display=0.0 dB`<br>`FILTER_TYPE (integer); options=0:Low-pass 4ᴾ, 1:Low-pass 3ᴾ, 2:Low-pass 2ᴾ, 3:Low-pass 1ᴾ, 4:High-pass 4ᴾ, 5:High-pass 3ᴾ, 6:High-pass 2ᴾ, 7:High-pass 1ᴾ, 8:Band-pass 4ᴾ, 9:Band-pass 2ᴾ, 10:Peak, 11:Notch, 12:HP 2ᴾ + LP 1ᴾ, 13:HP 1ᴾ + LP 2ᴾ, 14:HP 1ᴾ + LP 3ᴾ; display=HP 1ᴾ + LP 3ᴾ`<br>`Q_LIMIT (float); value=-10; range=[-30, 12]; display=-10.0 dB` |
| **XY** | `e84c96bc-6ff3-401b-af14-eddf9344c3e9` | 230 | `X (boolean); value=0; options=false, true; display=0.00 %`<br>`Y (boolean); value=0; options=false, true; display=0.00 %` |
| **Zero Crossings** | `5ff7e6e8-5158-46d4-9ba5-2d412750334c` | 231 | `MIN_FREQ (float); value=15.487; range=[15.487, 100]; display=20.0 Hz`<br>`MAX_FREQ (float); value=111.076; range=[30, 111.076]; display=5.00 kHz` |
| **by Scale** | `fc4504c5-73ec-4914-af09-6cb05bf9fccf` | 232 | `CONSTRAIN_MODE (integer); options=0:Quantize Up, 1:Smart Constrain, 2:Quantize Down; display=Quantize Down` |
| **by Semitone** | `845ff7e3-5e5b-4ffc-a8c7-531907e4709e` | 233 | — |
| **dB → Lin** | `20cd7bb0-81b2-444d-9b5c-49cf5aa2f341` | 234 | — |

## Installed Grid module catalog

| Module | Package ID |
| --- | --- |
| AD | `5b7ab937-4f09-41fc-a379-983fb597b2ff` |
| ADSR | `7e09068b-fee5-457e-afe4-7017661ebbd3` |
| AM/RM | `e1d4fdf5-057e-4c83-869e-db4ee322e4ce` |
| AND | `1e330c79-9a6f-4015-8dfa-da507c1bb15a` |
| AR | `9eaf8e7d-b8f7-4134-85c1-c7c77dd9fe92` |
| Abs | `895470df-c2de-417f-9113-8bb6fe948b6d` |
| Accents | `a0b3bd86-a4a9-4eac-83fc-468840332778` |
| Add | `57a6f72c-db9d-4a96-bc4b-d6a2bb8b656a` |
| All-pass Delay | `f435652c-2fd7-4edd-8b7a-ee97b0fd43a5` |
| All-pass | `b1682757-4fcf-4b5f-bfe7-58dd81d79954` |
| Amplify | `a6cd650b-c4de-46c6-8741-c07a0a9bfec2` |
| Array | `010ba490-caf6-4af6-93bd-82d9be63610c` |
| Attenuate | `cfc56753-defc-4324-8a68-bf747ff45508` |
| Audio In | `b2a6b111-7afd-4c95-b380-6de8125af980` |
| Audio Out | `af7b5503-c955-489e-9461-164107d56bb6` |
| Audio Sidechain | `59a10d46-c6a2-4676-a0fb-8a2923636d82` |
| Average | `2cbbf968-2a51-48ab-9e1f-ba665a52ea8b` |
| Bend | `c7d55e0b-33c6-4436-ba37-d1f1a0953893` |
| Bi → Uni | `97f5eff7-7619-4957-aa8f-5cfc353d56d6` |
| Bias | `c5aee529-9dce-406d-87cd-0f1cabcac13f` |
| Bite | `18b292a7-c11c-4014-b563-0784601e7cc8` |
| Blend | `0f2a027d-2bc3-4789-8a56-4d079a7e6137` |
| Button | `c0281e6e-3d55-4e86-8c9b-0ce8cf3db67d` |
| CC In | `311f3697-7323-46a0-a00b-1c51b12042e9` |
| CC Out | `131d870c-0df7-4f28-a536-cd13e82af404` |
| CV In | `632c2ab7-5c5a-493a-af69-ba4ada9997eb` |
| CV Out | `f137c16d-d9a3-471d-9e1d-586722988695` |
| CV Pitch In | `cc87d3c3-46f5-41e3-91d9-882243cdf717` |
| CV Pitch Out | `502771b2-1a4f-44c4-9038-03cac7da59e7` |
| Ceil | `321563fe-42e4-4353-84e2-bd95db6a00e4` |
| Chance | `fe6be8de-5abf-4825-99d7-c2127f039bb4` |
| Chebyshev | `0b9d73b3-796f-4cc0-b7af-d59e19df2827` |
| Chorus+ | `537b38d0-8ad3-4fa0-aa24-82c7c56c3d21` |
| Clip | `d9309744-b38c-4f40-95de-ee56bb073f4e` |
| Clock Divide | `a072e864-32de-4c4c-a334-2ed9afab0965` |
| Clock Quantize | `86d811e8-e1df-470b-9740-3bf3d924d87a` |
| Clock | `245af7f8-1137-4b44-abc3-b5e1f52fe016` |
| Comb | `b84241c5-b8b7-403f-8422-8195cf6d3478` |
| Comment | `b297dabd-144e-4106-b8da-15d08fa6b124` |
| Constant | `5412a6f2-9920-41b5-af13-ea64d266a26d` |
| Crossover-2 | `6ecd5ea8-9105-4350-af41-b2870ca54364` |
| Crossover-3 | `979bec96-fea9-4d7d-9657-65a447709b50` |
| Curve | `1093d01f-f6ba-4eef-8a62-3409d4d365ab` |
| Curves | `2302d0d8-afc0-4ed6-86ef-6d1dffeda6a2` |
| Delay | `e2e808c8-6b7e-4a00-9563-39e2f44177da` |
| Dice | `9f66c3b9-ca9b-4b62-8792-73fbec6464a4` |
| Diode | `8399cc4f-57a6-48aa-a38b-2dac60fd15f8` |
| Distortion | `6e8f9374-3393-4531-9f7e-571d0033ea94` |
| Divide | `21a1b455-fa76-4662-ad31-e89fbe0fcd65` |
| Dome | `fa194943-ad9a-4106-9aa9-9e2df5e44593` |
| = | `e4fda749-9129-4f03-ba7a-06099575ced6` |
| Exp | `eca1e042-b7ac-4f9e-863d-e5f32f6755da` |
| Exponents | `0ef176bd-a46a-424f-a163-2fc2276a9779` |
| Fizz | `d9e01995-14fc-4bae-a727-0fe2aa40c338` |
| Flanger+ | `00b09256-db30-40d5-b94f-c22477e49b5c` |
| Floor | `b0f4c3b2-eae2-44b3-805b-9d8d4c45ee34` |
| Follower RF | `0a1490cc-7df2-470c-b48e-6889b0f0361b` |
| Follower | `165fd92f-ed5e-4a54-97ed-99f334e28801` |
| Freq Shift+ | `904717d9-f24e-4742-9c75-b61ca0bf97bd` |
| Freq → Pitch | `fc1fba88-7413-41a4-9427-7251a44ac040` |
| Gain - Vol | `b1296326-cbf0-4797-9fc6-e2a6f2ce4a78` |
| Gain - dB | `b2c6ef93-8a14-4e10-b152-56bcee883e1c` |
| Gain In | `e470fc3b-4979-4c3b-aa79-27e6c49a3b88` |
| Gate In | `4e00fda6-20f6-45a9-9d7e-02867cf09b82` |
| Gate Length | `7b001029-62eb-4c40-81ab-13828622f3fd` |
| Gate Repeat | `71508287-dc35-4e62-b1a0-82ba2a2d8ef7` |
| Gates | `8d644ad7-8d77-4f05-a36e-04a57f719635` |
| ≥ | `d6008d9a-57b1-416a-ae5c-795dd386c674` |
| > | `7b681143-c276-49b9-9fed-1ce51d33aa39` |
| HW In | `d8195834-0238-4a18-bcba-d79efafa6f25` |
| HW Out | `49f0844b-e202-4011-b0a4-0d9f7c2ff41e` |
| Hard Clip | `5ae67be0-65a0-4905-84b4-1908baaf5613` |
| Heat | `cc13faed-d9c5-47b5-aca6-d0adbe0afdb5` |
| High-pass | `052cbe38-8ace-4ded-a4a9-de80a9f5fcea` |
| Hold | `9671cb0e-7272-4d50-9d2e-a207971983cf` |
| Howl | `5d528874-cf9f-48e8-9386-b3118a38d279` |
| Invert | `378e9b7d-0b95-4032-a12a-36d345550fab` |
| Key On | `6ba4eb9c-3ac6-4246-a4bd-192d395a3a58` |
| Keys Held | `ea6c6b9d-831b-4c05-a26b-2b1dadf81e0e` |
| LFO | `b89c1bce-203a-46be-8869-a44eb7868860` |
| LR Gain | `6a9e4b04-0e24-424f-abe3-a23b0744319a` |
| Label | `b3a19e19-da13-491d-b569-16ff5cbb109b` |
| Lag | `a4d23895-2761-476b-9aad-cbe372d286ea` |
| Latch | `61810948-1f33-4bc5-a8bb-d30c78e0afde` |
| ≤ | `a5080bc6-2ee1-4a97-ad52-511f2a88343f` |
| < | `c28a54ec-c679-4d09-b086-aa10fbae3b95` |
| Level Scaler | `800377c2-1f1c-4804-9440-4c6531047818` |
| Level | `0565644e-7e9f-45bf-bc34-8df52b5d7d80` |
| Lin → dB | `7091f45b-eb29-41e9-a285-c6173cf52288` |
| Log | `1c5671ab-6e13-4b60-90fd-b64142d4004d` |
| Logic Delay | `ec697982-2be4-4b87-88d4-333032f18577` |
| Long Delay | `f601a44c-8dcb-4ee7-9f2a-ce02ff07948e` |
| Low-pass LD | `85ca7753-049a-419a-bb37-d8c358b10932` |
| Low-pass MG | `a72eb152-884e-4bf0-bd22-d21e49fd3466` |
| Low-pass | `9747205f-2450-42da-89be-200b149b967b` |
| Merge | `c10b5ffa-0d10-4005-ad49-a39253ee26eb` |
| MinMax | `aaf43587-9228-4bb0-8743-8cbf411e6be7` |
| Mixer | `839e96da-cda4-45ce-b5a1-e0a40a176968` |
| Mod Delay | `a8d565fa-fcf5-4ede-bea9-90999f6e8406` |
| Modulator Out | `098ad9c6-b4c9-4ec1-887f-eaf588611056` |
| Multiply | `4a945068-35ff-469f-bc17-fda5d32b7baa` |
| N-Latch | `04685f05-a0bd-4cef-81f8-b59a2e2e16d1` |
| NAND | `328047a0-d0ff-47c6-93ac-44236e228157` |
| NOR | `5b278498-4ba5-415b-b159-337edebf952d` |
| NOT | `71d887c3-77b6-4ebd-86a9-a23f54a0d606` |
| Noise | `33344afa-c8fb-450f-8e82-65fd242a7837` |
| ≠ | `96507541-21a4-45a0-8bc6-48874e7de89e` |
| Note In | `06c1eac9-4d64-4748-8d52-8bf18324d1e7` |
| Note Out | `70baf51d-271c-43c3-b2de-c98fc48f326d` |
| OR | `3d31b4e4-ce56-4992-a793-39b362f8003a` |
| Octaver | `85c173a2-1eb3-4cc1-a19d-84bcb4bde00b` |
| Oscilloscope | `0a3b591d-a9b5-44dd-a6ee-a00794df4dc5` |
| Pan In | `3f482022-4a2c-4484-a5d8-d93a1d74e105` |
| Pan | `43600afd-7226-4408-bbb6-b7b9cc2a6cee` |
| Ø Bend | `c2d6358d-9053-49a3-9e1d-9b6c8d0bd539` |
| Ø Counter | `f9b5157c-0a41-403c-810b-9bbf9a133110` |
| Ø Formant | `9cab8245-ebbf-42ec-ba95-e7bcca4a9cab` |
| Phase In | `94d89ce0-4a98-4b95-be4a-36814d7b1855` |
| Ø Lag | `c03fc75f-c65b-452c-96ea-2ff8de806c26` |
| Ø Mirror | `de0334b8-93bd-463e-824b-dea397e90354` |
| Ø Pinch | `32323ba6-3a23-4c2d-a2c8-439961ba66ae` |
| Ø Pulse | `ecab3feb-20ad-494c-9a18-17536832002e` |
| Ø Reset | `d04bb748-5f66-4a4a-85d8-d3402c982e22` |
| Ø Reverse | `89f9e7d1-e36c-446f-937e-a881bf90c7c9` |
| Ø Saw | `4d7201c8-304a-4b42-95a2-5cc2fa945c18` |
| Ø Scaler | `53de290f-e7e0-4c71-95d4-dad2c8652691` |
| Ø Shift | `727cf275-dd41-4c5a-865d-efee322c04a7` |
| Ø Sine | `2d356600-6e66-49a2-91e5-c14397956a7a` |
| Ø Sinemod | `1c248b5d-47ef-401c-94c3-1f4f24d6a88a` |
| Ø Skew | `4f2ab665-8fca-4a03-b3b5-f85acdcf393a` |
| Ø Split | `f7272bf8-b86a-491c-b342-8eae1a792da4` |
| Ø Sync | `1cd61fc6-74a8-4117-bdb3-54bc8b033f8a` |
| Ø Triangle | `af9a7023-48a9-498e-ab27-33800bcf22f6` |
| Ø Window | `7ec54364-46c2-4303-b6c8-66905802f3b3` |
| Ø Wrap | `55792b95-b570-4513-b89d-4057c1af338b` |
| Phase-1 | `44da1c7d-5fef-4d7a-9b1c-739324a59a97` |
| Phaser+ | `50a03b86-dac7-431a-b923-3ab687a54d03` |
| Phasor | `2944a921-f9af-4781-9cf7-7fe98218fce3` |
| Pinch | `0df6f770-87b4-45fa-899b-d9e56c253255` |
| Pitch Buss | `88a039b7-13d3-40c0-9977-bfe37d06c60f` |
| Pitch Class | `7e371fc4-dae1-426b-8f0b-6dd980e63d31` |
| Pitch In | `b5ce2b79-e881-4105-ad80-4435cc57f75e` |
| Pitch Quantize | `70a58062-9175-4eec-9a25-b8f0f919773b` |
| Pitch Scaler | `c53fda13-4ed0-42fd-b410-19052ca6322d` |
| Pitch Shift | `69d1a916-2d39-4a4f-9334-7ec4def8eb83` |
| Pitch → Freq | `4ef26e44-92c8-42f0-a4fd-b70b3a3769cb` |
| Pitch → Ø | `f31bdee3-3f0c-4861-9a93-7514401a8a6f` |
| Pitch | `9adcd4b7-5dab-43cc-82da-ec5873ac3c72` |
| Pitches | `c9b6cefc-c467-45b6-aedb-ba02a9f887fe` |
| Pluck | `0ae4fef0-e859-4085-a100-448f5158eafb` |
| Poly → Mono | `0309fc67-0290-42b8-8ea3-625b333cb34c` |
| Power | `6808a887-6a5a-465d-ab48-84fb0995d2ca` |
| Pressure In | `2f6804b9-87a8-4c06-a61b-31e4171e1f2d` |
| Probabilities | `a65c43a5-f59a-460a-b22f-88571ac380ec` |
| Product | `93e8af3d-0cb4-41e4-b9cb-dc825b5fc5d7` |
| Pulse | `10c3be1f-ceb4-4bbc-bf35-af11285e58e0` |
| Push | `b7573eb6-2902-4f89-98cf-2c33b9f1b43b` |
| Quantize | `c1f45a63-edde-4c38-b588-efbd4c1e35ec` |
| Quantizer | `00e05a87-8b61-4540-9746-d8298406bc5a` |
| Rasp | `3a06f9a2-b1ec-42ff-bb55-35b42fcff581` |
| Ratio | `7ab5e7c4-671e-40de-8c06-21dd273c908c` |
| Reciprocal | `f4f35d7b-5fdd-40bd-98d8-c142e5ca66a8` |
| Recorder | `bdedc713-81ba-40b5-878c-a2e979ec2393` |
| Rectifier | `ac6de5ed-c143-4364-9989-3c7d299db380` |
| Ripple | `0b4317c5-7880-4515-ab71-b4607ddc8fdb` |
| Root Key | `1bc70e1f-5d9d-407e-a087-e222ef63089e` |
| Roots | `28166c20-3a55-45e8-8117-bfec9a62a4d4` |
| Round | `ae80ebb6-e84f-4cc9-848e-1dee19db8181` |
| S/H LFO | `965f7fc4-3f76-4e83-8870-98673cb0576a` |
| SVF | `2ddd3d4f-04b9-4ad5-a6f7-08e01df14c0f` |
| Sallen-Key | `726cd882-3d94-4140-b2b7-cfa7f416cc69` |
| Sample / Hold | `8214fd6c-5131-49d2-a9a6-709760a46b82` |
| Sampler | `40c0fe10-37ae-4d05-9ce1-d0bac5cd2b8e` |
| Saturator | `267e71c5-6aad-41f6-92da-3127e3bd1a25` |
| Sawtooth | `4ae6d37a-5412-4691-aa8b-261e94e60c59` |
| Scale Steps | `0015d740-8c68-4576-834e-2d4dabef24e1` |
| Scrawl | `9c1aa872-f271-4bd6-9f0d-37157399569c` |
| Segments | `953b71a0-c496-4cdc-8d50-843373d248b5` |
| Select In | `c6923eb3-e161-4eed-8a93-a4554287a77b` |
| Select Out | `4228f753-5073-4aa4-81c1-ec7f65b2ca23` |
| Shift Register | `749fc1c8-9f66-43bb-b11d-fbd7e5e84c02` |
| Shred | `cd8d3ec5-9655-4f5f-9a45-5aaf87edaa57` |
| Sine | `ca05aebd-ecaf-4d57-b0f6-c04ce81674c4` |
| Slope ↗ | `4da936f3-c96b-43f6-b716-6a70407a38fc` |
| Slope ↘ | `78e296cf-9ac8-415a-96c3-b7e924e061f3` |
| Slopes | `0b754e8c-cfb6-4399-aabe-c23d7e635f72` |
| Soar | `d7ca54e4-1d83-4dec-a40e-14d40fbd5ab5` |
| Spectrum | `9fe38e12-614b-470c-9dde-789fbde43f30` |
| Split | `61968cb5-c43f-41ce-bbb9-07e649dc38a5` |
| Step Access | `c74b57ac-0295-4daf-979a-b6248efbde7c` |
| Steps | `80d4de64-0ebc-4bb8-b448-74e57240f4a9` |
| Stereo Merge | `36096881-77f5-4ce1-b8c5-b3b21e6440f3` |
| Stereo Split | `842ae87e-de89-4583-9f24-43b91a218d1f` |
| Stereo Width | `a34edcba-25b3-4f07-86b2-81701b092d66` |
| Sub | `d1263096-fddf-438f-9c9f-ed9c1693e954` |
| Subtract | `1c779472-00d1-459c-9532-6b01d3baab1a` |
| Sum | `5b414321-7adb-4210-ab26-d2367a8b5d56` |
| Swarm | `faea6af4-72db-42c6-adac-0f74d8ebdbbf` |
| Timbre In | `21a6a402-2611-4311-b372-f36d36ad25d8` |
| Toggle In | `168a4502-2ec0-4222-b6cb-5a01875bc543` |
| Toggle Out | `f75deac4-c3d0-4630-a09c-4bbdac03c9d3` |
| Toggle | `5d016b16-be9c-4735-b9df-a533ee72528b` |
| Transfer | `3b18c07d-c4cb-4195-9c85-6b37ca1c048a` |
| Transport Playing | `9714df20-f4ea-4017-a874-4ccb554dd86e` |
| Transport | `997869ea-e649-4ac8-865e-bd4ac9e7b2a2` |
| Transpose | `35de4fbc-95f6-4719-911a-bc81a2d48df4` |
| Triangle | `9ab5d37c-f1ae-47a0-b85d-0f5b7c4fdb90` |
| Trigger | `d6aa9f53-8cc6-45a5-8fc7-f4ba97274b77` |
| Triggers | `e75916a0-2594-4181-88a4-b19fdb77c0eb` |
| Uni → Bi | `9d4c07ec-ea76-4c30-8c4e-ab94a192ec43` |
| Union | `df0a08cc-68b4-4fb2-a662-05cb09745e37` |
| VU Meter | `08d55d78-9240-43b9-9fe3-acde57ac1e60` |
| Value Readout | `8ac47e6d-1f50-41c0-91d1-0e4fa33e2f52` |
| Value Scaler | `512afe2b-0065-46b2-a65f-c8524b9e3552` |
| Value | `1faa5baf-6cdf-406a-b0e4-89b67501d982` |
| Velo Mult | `e74a80e4-9c17-49a8-9e84-98d07d6187bb` |
| Velocity In | `1ab8dfab-0671-406c-a423-5f362f5a62ca` |
| Voice Stack Info | `7a8675a4-be5a-4393-9257-c10b25358bfa` |
| Voice Stack Mix | `d58ced40-e61d-4988-8321-3a3456cdfe15` |
| Voice Stack Tog | `b96d7a4a-d0c8-4d4e-b069-98908e1fa2ea` |
| Vowels | `b4c661b9-576e-46ac-8be2-4974dd2f40ce` |
| Wavefolder | `aef23bda-40b6-4dba-86f5-044f617574e4` |
| Wavetable LFO | `d2524378-5019-40e7-af9f-08ec6aafce7e` |
| Wavetable | `19749bf6-0974-4356-9bce-6ab3b5a1af04` |
| XNOR | `c533df98-a287-4bdb-b1d9-1a694470721b` |
| XOR | `e6254ddf-6ba9-47f5-a6ac-402e2fc29a6c` |
| XP | `6cccc56b-cd93-435d-bae0-4d10c35c387a` |
| XY | `e84c96bc-6ff3-401b-af14-eddf9344c3e9` |
| Zero Crossings | `5ff7e6e8-5158-46d4-9ba5-2d412750334c` |
| by Scale | `fc4504c5-73ec-4914-af09-6cb05bf9fccf` |
| by Semitone | `845ff7e3-5e5b-4ffc-a8c7-531907e4709e` |
| dB → Lin | `20cd7bb0-81b2-444d-9b5c-49cf5aa2f341` |

## Session modification contract

1. Read `get_grid_capabilities`; stop if graph access is unavailable.
2. Read `get_grid_graph` and identify current module IDs, ports, cables, parameter ranges, options, and free coordinates.
3. Resolve a module by `search_grid_modules` and retain the returned UUID. Never derive or guess a package ID.
4. Present a small before/after graph diff. For cooperative requests, pass `cooperative: true`; otherwise pass `confirm: true`.
5. Insert at a free bounded coordinate with `grid_insert_module` or `grid_insert_modulator`. Connect only when the requested change requires it; leaving a new module unconnected preserves existing routing.
6. Re-read `get_grid_graph` after every mutation. Use the exact returned instance ID for subsequent parameter or connection edits.
7. Use `grid_set_modulator_parameter` for cataloged modulators and `grid_set_module_parameter` for other modules; both use native parameter ranges/options.
8. Use `grid_project_undo` for host-operation rollback; use `grid_shape_undo` only for preview-first selected-device parameter sessions.

## Refresh procedure

Regenerate this snapshot from a live bridge when the Bitwig installation, package catalog, bridge protocol, or project changes:

`get_grid_capabilities` → `get_grid_graph` → `graph-catalog` → capture Bitwig version → update revisioned JSON and this page.

Do not treat this file as permission to mutate a different project or selected device.
