# TH03 MAIN shared BOSS pattern selection: natural rejection loop

`boss_pattern_next()` now expresses its pattern rejection as a `do-while`
loop instead of `while(1)` plus an inner `break`:

```cpp
do {
    pattern = randring_far_next16_and(BOSS_PATTERN_VARIANTS_MASK);
} while(
    ((boss_pattern_previous + BOSS_PATTERN_RECENT_RADIUS) >= pattern) &&
    ((boss_pattern_previous - BOSS_PATTERN_RECENT_RADIUS) <= pattern)
);
```

This is the controller's actual repeat-until operation: at least one random
candidate is drawn, and every candidate inside the inclusive recent-pattern
window is rejected with another independent RNG draw. The subsequent previous-
pattern, frame, mode and pattern-index updates retain their original order.

The change is source-bound to `af1025a`. The complete `ba_srest` physical
object reproduces all 601 CODE bytes, 84 ordered native fields and seven
PUBLIC offsets in two independent original Turbo C++ 4.02 rounds. Both normal
MAIN links reproduce the original Japanese loaded image and ordered MZ
relocations.

Protected report: `.analysis/work/exatt-layout-af1025a/report.json`

SHA-256: `c75ba24faaed0e6e3fa2ec0d1104b2bba37adfe5e133ab46b7d204d999418313`


## Current-source revalidation (af1056c)

The original af1025a result established the `do-while` form before the shared
controller's later positive wait-frame scope. That later source revision used
`while(1)`/`break`; this pass reapplied the natural `do-while` under the current
controller shape and verified it again rather than assuming the older result
still transferred.

Two independent original TC4 4.02 rounds rebuilt both shared physical owners:
`ba_sring` and `ba_srest`. All 949 CODE bytes, 106 ordered native fields and
eight PUBLIC offsets match. Both normal MAIN links reproduce the original
Japanese loaded image and ordered relocations.

Current-source report: `.analysis/work/exatt-layout-af1056c/report.json`

SHA-256: `f23dfc1120fdf36091ccc6b890ac6a7382af9790b5b1662c06a830a13aa7dad5`
