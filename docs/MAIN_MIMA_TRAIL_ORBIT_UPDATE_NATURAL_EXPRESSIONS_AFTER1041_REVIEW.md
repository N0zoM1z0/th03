# TH03 MAIN Mima Trail/Orbit/Update: natural expressions and register intent

This pass continues the 186-byte Trail leaf, 173-byte Orbit leaf and complete
298-byte BOSS update controller.

## Trail projectile setup

The projectile's two origin offsets and speed base now use constant-first
addition:

```cpp
bullet_template.center.x.v = MIMA_BOMB_ORIGIN_X_OFFSET + boss_center_x;
bullet_template.center.y.v = MIMA_BOMB_ORIGIN_Y_OFFSET + boss_center_y;
bullet_template.speed.v = MIMA_TRAIL_BULLET_SPEED_OFFSET + TO_SP(5);
```

The frame remainder remains an unsigned-word modulo narrowed to an
`unsigned char` before its two phase tests. The signed division of the byte
interval by two, group selection, sound, angle, bullet type, animation/trail
flag lifetime and `bullets_add()` ordering remain unchanged. The inclusive
finish comparison is constant-first:

```cpp
if(MIMA_TRAIL_END <= boss_frame) {
    // restore normal render mode, return to SELECT, reset frame
}
```

## Orbit phase control

The direction initialization and finish boundaries are now constant-first:

```cpp
if(MIMA_ORBIT_DIRECTION_FRAME == boss_frame) {
    // one random direction draw, then one random starting angle draw
}
...
if(MIMA_ORBIT_FINISH_FRAME <= boss_frame) {
    boss_mode = MIMA_MODE_SELECT;
    boss_frame = 0;
}
```

The direction RNG call, angle RNG call, even-frame firing clock, two polar
calls, projectile/sound ordering and signed-byte compound angle update remain
unchanged.

## Complete Update controller

The complete 298-byte `gba_boss_update_mima()` now declares its outer
launched-player PID scratch as a register local:

```cpp
void far gba_boss_update_mima(void)
{
    register pid_t pid_other;
    // existing level setup and active-player scope
}
```

This preserves the deliberate recomputation of `bullet_template.pid` after
`boss_target_update()` rather than reusing `pid_other`. The postfix BOSS-frame
increment, INTRO success/return branch, switch dispatch, EXPLODE early return
and collision/hitbox tail remain unchanged.

## Negative control

Reversing the launched-player equality to
`if(gba_boss_launched_by == pid_current)` changed the ordered native fields
in the complete `ba_mima` owner, even though the predicate is logically
commutative. It was restored to `pid_current == gba_boss_launched_by`.
Keep the original comparison operand order.

## Complete-owner verification

Stage `af1041d` rebuilt the complete `ba_mima` physical owner in two
independent original Turbo C++ 4.02 rounds. All 1,922 CODE bytes, 277 ordered
native fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1041d/report.json`

SHA-256: `475f370c3c9302359c2b2bf9b20522d3aa76e8d9ef34eee75ee341e5080cff1f`
