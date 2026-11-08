# TH03 MAIN Mima orbit: natural finish predicate

The 173-byte `mima_pattern_orbit()` leaf now spells its finish comparison in
variable-first form:

```cpp
if(boss_frame >= MIMA_ORBIT_FINISH_FRAME) {
    boss_mode = MIMA_MODE_SELECT;
    boss_frame = 0;
}
```

This is the ordinary C++ reading of the same unsigned-word timer boundary.
The even-frame firing cadence, direction initialization, projectile emission
and signed-byte orbit-angle update remain unchanged.

Stage `af1030n` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030n/report.json`

SHA-256: `0d36f99e378b382fa6ec6fa9a9095f5da7142cc5bc7d19359ca8ed237dad590a`
