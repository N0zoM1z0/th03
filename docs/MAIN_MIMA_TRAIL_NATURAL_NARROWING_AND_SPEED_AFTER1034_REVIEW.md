# TH03 MAIN Mima Trail: natural byte narrowing and named speed offset

The 186-byte `mima_pattern_trail()` leaf now uses the destination type's
ordinary narrowing conversion for the modulo result:

```cpp
unsigned char remainder = (boss_frame % mima_trail_interval);
```

The division still operates on the original unsigned-word BOSS frame and
byte interval; only the stored result narrows to a byte before the two trail
phase comparisons. Removing the explicit `static_cast<unsigned char>` keeps
the original TC4 output.

The fixed `+ 8` in the trail projectile speed is now named
`MIMA_TRAIL_BULLET_SPEED_OFFSET`. The existing `TO_SP(5)` base, projectile
setup order, sound, trail-flag lifetime and finish transition are unchanged.

Stage `af1034a` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 4.02 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1034a/report.json`

SHA-256: `96e907f3c8f8113107763305c58c5e564b3aa2630157d5a7ee3953e6cfcc5806`
