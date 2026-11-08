# TH03 MAIN Yumemi Ring: phase guards, RNG branch and speed progression

The Yumemi Ring attack leaf now uses constant-first frame predicates and a
natural unsigned-word modulo cadence:

```cpp
if(YUMEMI_RING_INIT_FRAME == boss_frame) {
    // initial direction/radius state
}

if(YUMEMI_RING_WARNING_END > boss_frame) {
    bomb_axis_add(...);
    return;
} else if(YUMEMI_RING_BULLET_START > boss_frame) {
    return;
}

if(YUMEMI_RING_BULLET_START == boss_frame) {
    // explosion and alternate render mode
}

if(0 == (boss_frame % YUMEMI_RING_FIRE_PERIOD)) {
    // emit ring bullet
    yumemi_angle += yumemi_angle_delta;
    yumemi_speed_add += YUMEMI_RING_SPEED_ADD_STEP;
}

if(YUMEMI_RING_FINISH_AFTER < boss_frame) {
    // SELECT transition
}
```

The RNG branch now tests `0 == randring_far_next16_and(1)` without changing
the one RNG evaluation or the right/left signed-byte delta. The warning
`bomb_axis_add()` and return remain ahead of the quiet pre-fire interval; the
bullet-start explosion, ring emission, signed angle compound update, speed
increase and finish transition retain their original order.

The period-four unsigned-word ring cadence is expressed as `% period`; TC4
emits the same native low-bit test. The byte speed increment is also expressed
as compound `+=`, while the signed byte angle remains its original compound
update.

Stage `af1036m` rebuilt the complete `ba_yumem` physical owner in two
independent original TC4 4.02 rounds. All 2,358 CODE bytes, 343 ordered native
fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1036m/report.json`

SHA-256: `e033335f4ccd8007173723cf7f45032b9f08b6c5ebf8517f64b92587bb3f8b0e`
