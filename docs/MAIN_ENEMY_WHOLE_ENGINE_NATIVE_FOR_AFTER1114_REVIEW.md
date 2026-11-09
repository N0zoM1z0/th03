# TH03 MAIN — complete Enemy engine/formation source recovery (af1114e)

All **four** original Enemy Turbo C++ 4.02 physical owners were rebuilt
as one source-bound affected group: `eforna`, `efornb`, `eupda`, `eupdb`.
The full semantic code includes first-free Enemy allocation, ENEDAT script
formation streaming and randomized order, script interpreter/movement helpers,
reverse collision testing, sprite rendering and forty-entity frame updates.

The renderer's inactive/queued `continue` and update's two separate early
`continue` paths now use natural `for` headers, with their original signed
index and near pointer progression centralized rather than duplicated.
The ENEDAT formation parser, 256-formation RNG sequence and formation emitter
also use natural `for`, preserving each stream read, byte counter, independent
RNG draw and emission order. The reverse collision scan uses natural signed
`for`, and both original zero-height bounds are expressed directly as zero.
The first-free allocator and reverse collision pass admit native-exact prefix
near-pointer advancement. The movement helper initializes horizontal velocity
at its first actual use.

Real original TC4/TLINK stages `af1114a` (both full renderer/update passes),
`af1114b` (formation parser and RNG), `af1114c` (formation emitter and
reverse collision), `af1114d` (near-pointer progression and zero predicates),
and final `af1114e` (movement scratch and source comments) each passed two
independent original compiler and complete normal MAIN link rounds.
Both rounds match 3,325 original CODE bytes, 222 ordered native fields,
19 PUBLICs, the full Japanese MAIN loaded image and all 1,553 ordered MZ
relocations. Final source-linked receipt:
`.analysis/work/exatt-layout-af1114e/report.json`.

Fresh `af1114f` moved the ENEDAT script VM's player pointer declaration
into its use site. The real compiler changed the `efornb` physical CODE; the
attempt was rejected. The original uninitialized formation-previous value
and intentionally broken ENEDAT loop semantics remain, not silently fixed.
This is local source-native progress, not canonical Factory acceptance.
