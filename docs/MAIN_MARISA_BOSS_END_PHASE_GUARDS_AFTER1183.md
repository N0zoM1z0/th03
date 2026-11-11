# Marisa BOSS: exact terminal phase guards in three complete attacks

The full `ba_maris` BOSS now treats the unfinished final frame of its wide
four-column, narrow three-column, and 32-frame ring attacks as an early
return. The original Extra Attack calls, per-volley RNG order, warning
renderer flags, signed bullet divisions and ring sprite/template mutations
all remain in their original phase order. The three finish paths only
reset mode and frame after the appropriate original threshold.

Successive original TC4/TLINK stages `af1183d` (ring), `af1183e` (wide
columns) and final `af1183f` (narrow columns) each matched the full 1,431
CODE bytes, 199 literal native fields, nine PUBLIC offsets, and complete
Japanese MAIN loaded image and ordered MZ relocations in both compiler
rounds.

An independent `af1183a` attempt moved the main sprite-strip temporary
into a narrower post-guard lifetime. Its CODE changed and was rejected;
the original renderer local remains in its proven scope.

## Current Marisa attack and renderer control (2026-11-11)

`marisa_pattern_spread()` now guards both speed-layer volleys and their
byte-angle advance with a positive four-frame zero-remainder condition.
Off-cadence frames skip the fire block without resetting attack mode.
The wide-column family commits SELECT only at its original terminal
frame, and `marisa_pattern_ring()` uses an explicit 32-frame zero
remainder gate followed by positive completion at its original deadline.
`marisa_render_main()` returns early outside active attack mode after
drawing the main/optional hit sprite; the remaining flicker-strip path
retains its original VRAM offsets, sprite sizes and call order.

An experimental high-level-first dense-ring branch (`af1356d`) preserved
total CODE length but changed **39** byte locations, so it was reverted.
The signed byte-count division, cloud angle and RNG sequence stay in the
original low-level-first branch layout. Whole-owner stages `af1356a`,
`af1356b`, `af1356c`, `af1356e` and current `af1356f` each matched the
original in two Turbo C++ rounds. `af1356f` proves **1,431 CODE bytes,
199 ordered native fields and 9 PUBLICs**. Joint `af1356g` recompiles
Marisa BOSS, Bullet, shared BOSS (two objects), Marisa Extra Attack and
SE service: **5,861 CODE bytes, 554 fields and 44 PUBLICs**, both
normal MAIN links and ordered relocations exact.

Source proof: `.analysis/work/exatt-layout-af1356f/report.json`, SHA-256
`86677d1703bc76d25df61aa000ce8e5e0821b289adeb95e313c5cc534514ea07`.
Joint proof: `.analysis/work/exatt-layout-af1356g/report.json`, SHA-256
`16f4e3cf8143eff2c82404b47bbc9f93db51aa76ceecb90139bbad3c2ed31d05`.
