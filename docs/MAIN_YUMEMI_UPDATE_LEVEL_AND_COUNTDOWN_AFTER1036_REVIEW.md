# TH03 MAIN Yumemi update: level formulas, origin setup and countdowns

The complete 368-byte `gba_boss_update_yumemi()` now uses constant-first
level formulas for its ring speed/count, aimed speed and chase limit:

```cpp
yumemi_ring_speed = YUMEMI_LEVEL_RING_BASE +
    (gba_boss_level / YUMEMI_LEVEL_HALF);
yumemi_ring_count = YUMEMI_LEVEL_RING_BASE +
    (gba_boss_level / YUMEMI_LEVEL_HALF);
yumemi_aimed_speed_base = YUMEMI_LEVEL_AIMED_SPEED_BASE + gba_boss_level;
yumemi_chase_until = YUMEMI_LEVEL_CHASE_BASE +
    (YUMEMI_LEVEL_CHASE_MULTIPLIER * gba_boss_level);
```

The cross interval and rain interval remain their original base-minus-level
and base-minus-level/half formulas. Replacing the three divisions by two
with `gba_boss_level >> 1` changed the complete `ba_yumem` CODE (negative
`af1036l`); retain the natural division expressions.

The active-player update now spells its frame increment as postfix, puts the
X origin offset first, and uses constant-first INTRO sound/completion tests.
The sound checks still precede the completion test. The two countdown guards
use direct truth tests:

```cpp
if(boss_effect_radius) {
    boss_effect_radius -= YUMEMI_EFFECT_RADIUS_DECAY;
}
if(boss_render_frame) {
    boss_render_frame--;
}
```

The byte render-frame decrement remains postfix; a prior independent probe
showed prefix changes original CODE. The effect-radius and render-frame
countdowns remain after the switch and before collision-map/hitbox work.

Stage `af1036k` rebuilt the complete `ba_yumem` physical owner in two
independent original TC4 4.02 rounds. All 2,358 CODE bytes, 343 ordered native
fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1036k/report.json`

SHA-256: `963f21a61f4fad35c6460d36866fea0ac4a3874c6ba90ee8dac7760bfbaed082`
