# TH03 MAIN Chiyuri update: power-of-two render cadence

The 613-byte `gba_boss_update_chiyuri()` now spells its four-frame animation
cadence as a low-bit test:

```cpp
boss_render_frame += (
    (round_or_result_frame & (CHIYURI_RENDER_ANIM_PERIOD - 1)) == 0
);
```

`round_or_result_frame` is an unsigned 16-bit clock and the period is four, so
the mask tests exactly the same cadence as `% 4 == 0`. Turbo C++ 4.02 already
lowered the remainder form to `TEST ..., 3`; the mask spelling therefore
retains the original native instruction sequence while expressing the
power-of-two property directly.

Stage `af1030c` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Two nearby prefix-increment alternatives were also tried and rejected:
`++boss_pattern_i` changed the byte increment from direct memory `INC` to
load/increment/store because the updated value feeds the following comparison;
`--boss_render_mode` changed the complete owner as well. Both were reverted.

Protected report: `.analysis/work/exatt-layout-af1030c/report.json`

SHA-256: `e8c2e6b14dffd6154a7c51b4249b327a15545954032e7f631f4969f96d4b2b12`
