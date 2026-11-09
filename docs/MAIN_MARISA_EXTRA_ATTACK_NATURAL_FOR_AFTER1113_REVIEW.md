# TH03 MAIN — complete Marisa Extra Attack entity controllers (af1113c)

The original five-function `ex_maris` P_EXATT_TEXT Turbo C++ 4.02 owner
contains both first-free 14-slot Extra Attack allocators, the sprite/beam
renderer, the entire collision/update state machine and its own full render
walk. All four physical entity traversals now use natural `for` headers,
with the original signed index and near pointer incrementing at the end of
each iteration. Most importantly, the long live update now sends all **three**
`continue` paths to the shared `for` progression; it no longer duplicates
pointer/index mutations in the free, beam-termination and flight-arrival
paths. Spawn timing, collision heights, RNG draws, object states and frame
increments remain in their original order. The update's physical pointer
initializes after the collision-width setup at first use.

Successive original compiler/full normal linker runs `af1113a` (both
allocators and renderer), `af1113b` (the complete state/collision update),
and `af1113c` (first-use near pointer) each matched in two independent TC4
rounds. This includes all 676 original CODE bytes, 35 ordered native fields,
five PUBLICs, the full Japanese MAIN loaded image and all 1,553 ordered MZ
relocations. The final source-bound native receipt is
`.analysis/work/exatt-layout-af1113c/report.json`.

A separate `af1113d` trial moved the update's signed local `i` declaration
into its `for` header. TC4 changed CODE; restoring its original local lifetime
restored exactness. No full cold replay, byte patching or canonical Factory
credit is claimed.
