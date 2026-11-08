# TH03 MAIN Reimu Update: positive INTRO completion branch

The INTRO path in the complete Reimu update controller now expresses
completion as the positive equality branch:

```cpp
if(boss_mode == REIMU_MODE_INTRO) {
    if(boss_frame == REIMU_INTRO_END_FRAME) {
        boss_frame = 0;
        boss_mode = REIMU_MODE_SELECT;
    } else {
        return;
    }
}
```

The old form returned when the frame differed from the completion constant,
then reset the frame and selected mode on equality. The positive branch keeps
the same reset and mode assignment and preserves the non-completion early
return. The separate SELECT test still follows the INTRO block, so the newly
selected mode immediately reaches the existing `boss_pattern_next()` path on
the same update as before.

Stage `af1033i` rebuilt the complete `ba_reimu` physical owner in two
independent original TC4 4.02 rounds. All 2,020 CODE bytes, 270 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1033i/report.json`

SHA-256: `92dedb25232de17195d8040315dc015125b49b360e056e6799c8709f0868748c`
