# TH03 MAIN Kotohime: Radial Burst arithmetic, scratch lifetimes and Update

This pass continues both the 302-byte `kotohime_pattern_radial_burst()` leaf
and the complete 332-byte `gba_boss_update_kotohime()` controller.

## Radial Burst arithmetic and variable lifetimes

The nested projectile traversal now declares its register indices and
scratch values once in outer-to-inner order within the release branch:

```cpp
register int center_i;
register int bullet_i;
register int x;
register int y;
register unsigned char center_angle;
for(center_i = 0; center_i < kotohime_orbit_count; ++center_i) {
    center_angle = boss_move_phase +
        ((KOTOHIME_FULL_TURN_STEPS * center_i) / kotohime_orbit_count);
    x = polar(boss_center_x, boss_effect_radius, CosTable8[center_angle]);
    y = polar(boss_center_y, boss_effect_radius, SinTable8[center_angle]);
    bullet_template.center.x.v = x;
    bullet_template.center.y.v = y;

    for(bullet_i = 0; bullet_i < kotohime_burst_count; ++bullet_i) {
        bullet_template.angle =
            KOTOHIME_BURST_CENTER_ANGLE_OFFSET + center_angle +
            ((KOTOHIME_BURST_HALF_TURN_STEPS * bullet_i) / kotohime_burst_count);
        bullet_template.speed.v = KOTOHIME_BURST_SPEED_BASE +
            ((KOTOHIME_BURST_SPEED_SCALE * bullet_i) / kotohime_burst_count);
        bullets_add();
    }
}
```

The DI/SI roles remain outer center then inner bullet. `bullet_i` resets for
each center. The `x`, `y` and byte `center_angle` scratch are reused across
outer iterations rather than declared inside the loop body. These lifetime
and declaration-order changes compile to the same complete owner.

Three signed multiply expressions now put their named scale first:
`FULL_TURN_STEPS * center_i`, `HALF_TURN_STEPS * bullet_i`, and
`BURST_SPEED_SCALE * bullet_i`. The burst angle addition is also exact with
the named center offset first, then the center angle, then the divided local
angle. Signed 16-bit multiplication/division still occurs before byte-angle
truncation; polar calls, coordinate stores and projectile order remain exact.

## Update controller

All six additive difficulty formulas now use base-first additions:

- Random ring speed and orbit count
- Slow and fast aimed speeds
- Pellet speed
- Radial burst count

The level-derived division expressions remain actual divisions. The 332-byte
controller also uses postfix `boss_frame++` and a constant-first INTRO finish
comparison. The active-player scope, bullet PID/target helper ordering, INTRO
and EXPLODE early returns, mode dispatch and collision/hitbox tail remain
unchanged.

## Negative controls

The radial phase byte's original AL-mediated load/add/store remains required.
The following apparently natural direct assignments changed complete CODE
and were rejected:

```cpp
boss_move_phase = boss_move_phase + (unsigned char)0xFC;
boss_move_phase = boss_move_phase - 4;
boss_move_phase = (unsigned char)(boss_move_phase - 4);
```

Keep the original `_AL = boss_move_phase; _AL += (unsigned char)0xFC;
boss_move_phase = _AL;` sequence. The earlier `boss_move_phase -= 4`
negative result is also documented in the after1033 Radial review.

## Complete-owner verification

Stage `af1037r` rebuilt the complete `ba_koto` physical owner in two
independent original TC4 4.02 rounds. All 1,840 CODE bytes, 262 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1037r/report.json`

SHA-256: `1789957b2e67391ec9bcec84d01368108226819d1f7fd6f4dde9bfa1a629ef07`
