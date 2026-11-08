# TH03 MAIN Mima Trail: variable-first finish predicate

The 186-byte `mima_pattern_trail()` leaf now expresses its finish boundary as:

```cpp
if(boss_frame >= MIMA_TRAIL_END) {
    boss_render_mode = MIMA_RMODE_NORMAL;
    boss_mode = MIMA_MODE_SELECT;
    boss_frame = 0;
}
```

This is the natural variable-first spelling of the same unsigned-word frame
comparison. The trail bullet setup, sound, trail flag lifetime and exact finish
frame remain unchanged.

Stage `af1030v` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030v/report.json`

SHA-256: `b830cdf8dfc6858d1c58789d6afffd0e218db1feeb8d3deceaf4caf8b5920e3b`
