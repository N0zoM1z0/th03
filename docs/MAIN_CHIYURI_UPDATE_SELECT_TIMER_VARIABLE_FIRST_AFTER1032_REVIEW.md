# TH03 MAIN Chiyuri Update: variable-first SELECT timer guard

The SELECT timer test in the 613-byte `gba_boss_update_chiyuri()` controller
now reads naturally as:

```cpp
if(boss_frame >= CHIYURI_SELECT_TIME_AT) {
    boss_frame = 0;
    boss_mode = (randring_far_next16_and(0x0F) + 2);
    boss_pattern_i++;
    if(boss_pattern_i > boss_pattern_count) {
        boss_mode = CHIYURI_MODE_DESCEND;
    }
}
```

The unsigned 16-bit clock and inclusive selection threshold are unchanged.
The random mode selection, byte postfix pattern counter, overflow/finish
check and descent override remain in their original order.

Stage `af1032c` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 4.02 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1032c/report.json`

SHA-256: `0274807e1cd5d4ecf93a350d1a62dc04409c6bd4eee0f3e943a9c766fa8b415e`
