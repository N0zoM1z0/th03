# TH03 MAIN Chiyuri Rings: variable-first finish predicate

The 208-byte `chiyuri_pattern_rings()` leaf now spells its attack finish
boundary as:

```cpp
if(boss_frame >= CHIYURI_PATTERN_END_AT) {
    boss_mode = CHIYURI_MODE_SELECT;
    boss_frame = 0;
    boss_render_mode = CHIYURI_POST_ATTACK_PALETTE;
}
```

This is the natural variable-first form of the same unsigned-word frame
comparison. The warning bomb still precedes the finish transition, and the
main ring plus optional four-pellet burst retain their original order.

Stage `af1030t` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030t/report.json`

SHA-256: `48e14edb2b2405b78692bc231195205a0a7a18778cd2fdfea98e96d9a5225a8f`
