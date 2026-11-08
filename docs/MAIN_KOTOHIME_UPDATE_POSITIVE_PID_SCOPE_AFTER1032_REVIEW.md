# TH03 MAIN Kotohime Update: positive launched-player scope

The complete 332-byte `gba_boss_update_kotohime()` controller now scopes its
active update under the positive launched-player predicate:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_other = (1 - pid_current);
    boss_target_update();
    bullet_template.pid = pid_other;
    ++boss_frame;

    switch(boss_mode) {
        // INTRO, SELECT, Random Ring, Aimed Ring, Pellet Arc, Radial,
        // DESCEND and EXPLODE
    }

    // collision map and hitbox/HP tail
}
```

Previously a mismatch returned before the controller, while the active path
ran unconditionally after the guard. The positive scope keeps the complete
mode switch and collision tail together; a non-launched player now simply
falls through to the implicit return. The per-character `pid_other` setup,
INTRO early return, EXPLODE early return and all pattern dispatch/collision
operations remain in their original order.

Stage `af1032p` rebuilt the complete `ba_koto` physical owner in two
independent original TC4 4.02 rounds. All 1,840 CODE bytes, 262 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1032p/report.json`

SHA-256: `140595d6715f9b86708ef7c2547bbf98804fbf2da0b963466cfaf4ffda2d0601`
