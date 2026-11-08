# TH03 MAIN Chiyuri Cardinal: variable-first finish predicate

The 352-byte Cardinal leaf now expresses the attack finish boundary as:

```cpp
else if(boss_frame >= CHIYURI_PATTERN_END_AT) {
    boss_mode = CHIYURI_MODE_SELECT;
    boss_frame = 0;
    boss_render_mode = CHIYURI_POST_ATTACK_PALETTE;
}
```

This is the natural variable-first spelling of the same unsigned-word frame
comparison. The first-frame cross setup remains mutually exclusive with the
finish transition, and the final cardinal volley still emits on its original
tick before the mode reset.

Stage `af1030s` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030s/report.json`

SHA-256: `9100b0f3029b532b2323925a6d89e78e3d268f5e393956ccb9b3a10cb572b92a`
