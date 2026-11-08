# TH03 MAIN Chiyuri Update: variable-first palette-cycle guard

The SELECT branch in the 613-byte `gba_boss_update_chiyuri()` controller now
places the mutable render-state byte on the left of its palette-cycle test:

```cpp
if(boss_render_mode == CHIYURI_PALETTE_CYCLE_START) {
    random_i = (randring_far_next16_mod(5) << 1);
    boss_center_x = chiyuri_boss_x_words[random_i];
    boss_center_y = chiyuri_boss_y_words[random_i];
    boss_move_phase = CHIYURI_PALETTE_CYCLE_START;
}
```

The five-way random selection is still evaluated once, the doubled byte index
still selects the same X/Y pair, and the palette phase is initialized after
both center coordinates. This is the ordinary variable-first C++ spelling;
TC4 emits the same complete owner.

Stage `af1032e` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 4.02 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1032e/report.json`

SHA-256: `9734048fd14398db525bc12b2dfd785b1b391c982220876d795268c14cc78cd2`
