# TH03 MAIN Mima level scaling and template initialization

The complete Mima BOSS source now uses constant-first arithmetic for all
seven difficulty-derived pattern parameters in `gba_boss_update_mima()`:

```cpp
mima_bullet_speed = MIMA_LEVEL_BULLET_BASE + gba_boss_level;
mima_random_count = MIMA_LEVEL_RANDOM_COUNT_BASE +
    (gba_boss_level / MIMA_LEVEL_QUARTER);
mima_random_speed = MIMA_LEVEL_BULLET_BASE + gba_boss_level;
mima_trail_interval = MIMA_LEVEL_TRAIL_INTERVAL_BASE - (2 * gba_boss_level);
mima_pellet_speed = MIMA_LEVEL_PELLET_SPEED_BASE + gba_boss_level;
mima_pellet_until = MIMA_LEVEL_PELLET_UNTIL_BASE +
    (MIMA_LEVEL_PELLET_UNTIL_MULTIPLIER * gba_boss_level);
mima_orbit_speed = MIMA_LEVEL_ORBIT_SPEED_BASE + gba_boss_level;
```

The original division by four remains a division. The `gba_boss_level >> 2`
substitution changed the complete physical owner's CODE and was rejected.
Constant-first operand ordering for the two multiplications (`2 * level`
and `MIMA_LEVEL_PELLET_UNTIL_MULTIPLIER * level`) is exact, as are all
constant-first additions. The `boss_update_start()` gate and assignment
sequence remain unchanged.

The 79-byte Pascal `boss_mima_template_init()` now uses a constant-first
player test:

```cpp
if(0 != player_id) {
    p->sprite_offset += MIMA_TEMPLATE_PLAYER2_OFF;
}
```

This is exact and leaves the pointer-based initialization, all field stores,
and the player-two sprite adjustment in their original order.

A superficially more explicit assignment was also tested:

```cpp
p->sprite_offset = (p->sprite_offset + MIMA_TEMPLATE_PLAYER2_OFF);
```

That form changes the complete owner. Keep the compound `+=` operation.

Stage `af1035y` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 4.02 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1035y/report.json`

SHA-256: `5695f6c45a11dcc9f4f4a35214c4a255775cde06ef1c1f659520d38b17ce7452`
