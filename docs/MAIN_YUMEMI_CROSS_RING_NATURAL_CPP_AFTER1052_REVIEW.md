# TH03 MAIN Yumemi four-way cross-ring producer: natural C++ after1052

The 130-byte `yumemi_pattern_cross_rings()` leaf now expresses its four
independently randomized bullet positions with natural base-first arithmetic.
The four original angle draws and `bullets_add()` calls remain separate and
in their original order:

```cpp
bullet_template.center.y.v =
    -YUMEMI_CROSS_RING_DISPLACEMENT + boss_center_y;
...
bullet_template.center.y.v =
    YUMEMI_CROSS_RING_DISPLACEMENT + boss_center_y;
...
bullet_template.center.x.v =
    -YUMEMI_CROSS_RING_DISPLACEMENT + boss_center_x;
...
bullet_template.center.x.v =
    YUMEMI_CROSS_RING_DISPLACEMENT + boss_center_x;
```

The interval gate now uses the natural unsigned remainder truth test:

```cpp
if(!(boss_frame % yumemi_cross_interval)) {
    // one type RNG draw, then four angle RNG draws and four bullet adds
}
```

The finish-frame comparison remains constant-first. The call to
`boss_move_sine()` still occurs before the cadence check; the group, speed,
type and bullet call order is unchanged.

## Complete original-owner verification

Stage `af1052f` rebuilt the complete 2,358-byte `ba_yumem` physical object in
two independent original Turbo C++ 4.02 rounds. All 343 ordered native
fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The other 98
original game objects and CRT were reused; no full cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1052f/report.json`

SHA-256: `640d4879357499256fff192f2a6869c133e37e8100bc8b47c27f634cf96c82e4`

This is natural-C++ recovery in an already source-owned pattern leaf, not new
unique CODE ownership, raw vendor OMF packet identity or canonical packed-game
acceptance.
