# TH03 MAIN Mima orbit: constant-first finish comparison

`mima_pattern_orbit()` now writes its terminal frame check in the same
constant-first form used by other recovered BOSS phase tests:

```cpp
if(MIMA_ORBIT_FINISH_FRAME <= boss_frame) {
    boss_mode = MIMA_MODE_SELECT;
    boss_frame = 0;
}
```

This remains an inclusive end-frame check. The orbit still moves the boss
before selecting the initial signed rotation, fires on the original even
clock cadence, emits the same pellet-cloud ring, advances the byte angle by
the signed delta after `bullets_add()`, and only then checks the finish frame.
No bullet order or phase lifetime was changed.

Stage `af1026d` rebuilt the complete `ba_mima` physical owner in two
independent original Turbo C++ 4.02 rounds. All 1,922 CODE bytes, 277 ordered
native fields and nine PUBLIC offsets match. Both normal MAIN links reproduce
the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1026d/report.json`

SHA-256: `40816e7755ae26296e652f914ced186e3ae99f685c2a4142e3b35032139bd6a8`
