# TH03 MAIN Kotohime Pellet Arc: variable-first finish predicate

The 302-byte `kotohime_pattern_pellet_arc()` leaf now expresses its unsigned
word-timer finish boundary as:

```cpp
if(boss_frame >= KOTOHIME_PELLET_FINISH_FRAME) {
    boss_mode = KOTOHIME_MODE_SELECT;
    boss_frame = 0;
}
```

This is the natural variable-first form of the same completion threshold.
The arc's center/side pellet ordering, signed subpixel offsets, speed and
angle setup remain unchanged.

Stage `af1030w` rebuilt the complete `ba_koto` physical owner in two
independent original TC4 rounds. All 1,840 CODE bytes, 262 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030w/report.json`

SHA-256: `0d278a8af3b6088ea39123e5d986be1a35ded7b24d31ec91e038277fa7c1c01e`
