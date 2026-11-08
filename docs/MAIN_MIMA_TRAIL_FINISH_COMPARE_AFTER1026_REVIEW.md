# TH03 MAIN Mima Trail: constant-first finish comparison

`mima_pattern_trail()` now spells its inclusive end-frame test with the named
phase threshold first:

```cpp
if(MIMA_TRAIL_END <= boss_frame) {
    boss_render_mode = MIMA_RMODE_NORMAL;
    boss_mode = MIMA_MODE_SELECT;
    boss_frame = 0;
}
```

The modulo result is still narrowed to an unsigned byte before either trail
phase comparison. The two phases, second-ring group choice, sound, bullet
origin, speed, type, animation/trail flags and `bullets_add()` order are
unchanged. The terminal transition remains after the optional shot.

Stage `af1026g` rebuilt the complete `ba_mima` physical owner in two
independent original Turbo C++ 4.02 rounds. All 1,922 CODE bytes, 277 ordered
native fields and nine PUBLIC offsets match. Both normal MAIN links reproduce
the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1026g/report.json`

SHA-256: `21469d5d69f62d20ed50fc7649e616171602df5ee0da47f3212a02f92e1427c7`
