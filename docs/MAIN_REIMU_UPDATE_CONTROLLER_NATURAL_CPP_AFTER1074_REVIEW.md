# TH03 MAIN Reimu Update Controller: local PID, frame and phase guards (af1074k)

This pass recovers the complete 296-byte far `gba_boss_update_reimu()`
controller rather than stopping at its smaller attack leaves. It changes the
level-derived setup expressions, scopes the other-player PID to the active
player path, simplifies the INTRO completion guard, and uses natural
variable-first mode comparisons. The full switch dispatch and collision /
hitbox tail remain in place.

## Level-derived setup

The setup still runs only when `boss_update_start()` is true, and retains the
original signed division for the level-derived interval and orbit count:

```cpp
if(boss_update_start()) {
    reimu_cloud_interval = (5 - (gba_boss_level / 5));
    reimu_unused_param = (gba_boss_level + 0x18);
    reimu_bullet_speed = ((2 * gba_boss_level) + 0x28);
    reimu_orbit_count = ((gba_boss_level / 8) + 4);
    reimu_ring_speed = (gba_boss_level + 0x10);
    reimu_ring_count = (gba_boss_level + 0x10);
}
```

Multiplying the byte level by two with `2 * gba_boss_level` is exact and
readable. The right-shift replacement for `/ 8` was tested and rejected; keep
the division because the original level type's signedness matters to TC4
codegen. Chaining the identical ring-speed/ring-count assignments was also
tested and changed the owner, so both assignments remain explicit.

## Active-player scope and PID lifetime

The inactive-player path still returns before target tracking or frame
advancement:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}

pid_t pid_other = 1 - pid_current;
boss_target_update();
boss_frame += 1;
```

The ordinary `pid_t` local is now initialized at its first use, after the
inactive-player guard, rather than declared at function entry and assigned in
a separate statement. Removing `register` still matches the complete owner.
The unparenthesized `1 - pid_current` initializer is the maintained form.
XOR is not a substitute here: `pid_current ^ 1` changed CODE.

The frame increment is `+= 1`. Prefix `++boss_frame` was independently
verified too; explicit `boss_frame = boss_frame + 1` changed CODE. Both
accepted forms preserve the original word increment and the maintained
compound form is used in the current source.

## INTRO and SELECT state transitions

The INTRO path now uses a direct early-return guard:

```cpp
if(boss_mode == REIMU_MODE_INTRO) {
    if(boss_frame != REIMU_INTRO_END_FRAME) {
        return;
    }
    boss_frame = 0;
    boss_mode = REIMU_MODE_SELECT;
}

if(boss_mode == REIMU_MODE_SELECT) {
    boss_pattern_next();
}
```

This preserves the update ordering: target tracking and frame advancement
happen before the INTRO check; a nonterminal INTRO frame returns; the terminal
frame resets to SELECT and immediately calls `boss_pattern_next()`.
Variable-first mode comparisons are used for both INTRO and SELECT.

The EXPLODE return remains a `switch` case. Hoisting it into a separate guard
before the switch was tested and changed CODE. Likewise, the complete mode
switch and the following collision-map / hitbox tail remain in their original
order.

## Collision and HP tail

The `collmap_center`, striped tile dimensions, PID, `hitbox` origin/radius,
explosion-skip flag, `hitbox_hittest()`, HP subtraction and
`boss_hittest_end()` operations remain ordered as before. In particular,
`boss_hp -= boss_hit` is retained; spelling it as
`boss_hp = boss_hp - boss_hit` changes the complete physical owner.

## Complete original-owner verification

Stage `af1074k` rebuilt the complete `ba_reimu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,020 CODE bytes, 270 ordered
native fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1074k/report.json`

SHA-256: `c323510a9cc84d763d4b404d43097c3a952fca7c95f29b1bdf2133e8ed5ef46c`

Source SHA-256: `488739dbd18816b91c005b8659bb07f378d5674315b0a70e3662ff7462d97a58`

## Joint current-source integration

Stage `af1074n` rebuilt Reimu, Yumemi and Chiyuri together in two independent
original TC4 rounds: 7,032 CODE bytes, 994 ordered native fields and 30 PUBLIC
offsets match. Both complete normal Japanese MAIN links reproduce the
original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1074n/report.json`

SHA-256: `badc35d10c7959d8afa7e11cb34b8a05d7ce0f4966feca573617f07b3609d91f`

This is scoped original-toolchain evidence, not a Factory Oracle receipt,
raw vendor OMF identity claim, or canonical packed-file acceptance.
