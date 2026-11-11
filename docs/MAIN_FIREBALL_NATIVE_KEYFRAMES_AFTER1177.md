# Fireball engine: native keyframes and complete entity index lifetimes

The complete `e_fireb` physical owner now expresses the explosion collision
keyframe transitions as individual finished-state returns rather than an
`else if` chain. Its 24-slot update and the reverse 24-slot fireball collision
scan declare their signed indices in their natural `for` headers. These
changes preserve the original transfer and clipping labels, the exact
RNG/chain reward order and the historically uninitialized `chain_slot` value;
the latter is gameplay-visible and was not initialized as a source cleanup.

The final `af1177g` native TC4/TLINK stage reproduces the complete 1,555
CODE bytes, 115 ordered native fields, ten PUBLICs and the Japanese MAIN
image/relocations in both original compiler rounds. The independent
`af1177d` trial showed that the **allocator** index cannot be narrowed,
although the complete movement and collision indices can (`af1177e`).
Similarly, narrowing the byte explosion cel local (`af1177f`) changed CODE.

## Current charged-chain Extra Attack gate (2026-11-11)

`chain_fire_charged_exatt()` now returns immediately if the original
byte charge is below its round-speed-dependent threshold. On a charged
slot it still zeros the same indexed array element before passing the
existing entity's two subpixel centers and one-byte player ID to
`exatt_add()`. The signed 16-bit threshold division and original
historically uninitialized caller `chain_slot` are unchanged.

An isolated negative trial `af1361i` cached the array address in a
`uint8_t near *` and changed complete-object CODE. The original direct
indexing is retained; source `af1361h` proved the early exit and current
`af1361j` proved the commented current source. Both original TC4 rounds
reproduce **1,555 CODE bytes, 115 ordered native fields, 10 PUBLICs**
with exact normal Japanese MAIN images and ordered relocations.

Consumer stage `af1361k` recompiles Fireball, Explosion collision,
both Combo objects, shared Extra Attack, Gauge, Rikako BOSS and Extra
Attack, and Bullet: **8,323 CODE bytes, 681 ordered fields, 51 PUBLICs**.
Only these affected physical objects were recompiled.

Current proof: `.analysis/work/exatt-layout-af1361j/report.json`, SHA-256
`f211cb584ed18c6eeeb183f092e71a04a6a41c012f596f5315c0cba867febe54`.
Joint proof: `.analysis/work/exatt-layout-af1361k/report.json`, SHA-256
`ae251112d8c0c9d415af39d44759243b1487da99ab76cb9456b4aa98c64df4b0`.
