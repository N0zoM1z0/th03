# TH03 MAIN Chiyuri update: byte-phase truth tests

The update controller now uses direct truth tests for both byte-valued phase
fields:

```cpp
if(boss_move_phase) {
    boss_move_phase--;
    if(boss_move_phase) {
        bomb_palette_step((boss_move_phase * 16), pid_other);
    }
}
```

The two fields are unsigned bytes, so testing them directly is equivalent to
comparing against zero. Keeping the postfix decrement and the nested second
test is important: the byte-memory decrement and its subsequent reload remain
in the original order.

Stage `af1030e` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030e/report.json`

SHA-256: `d9e8554255f0b1e7f28df35157827484b31dac5c5280d3e473da05150f7f5c73`
