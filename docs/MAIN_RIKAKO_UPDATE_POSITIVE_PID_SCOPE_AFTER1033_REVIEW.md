# TH03 MAIN Rikako Update: positive launched-player scope

The complete 285-byte `gba_boss_update_rikako()` controller now scopes its
active path under the positive launched-player predicate:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_other = (1 - pid_current);
    bullet_template.pid = pid_other;
    boss_target_update();
    ++boss_frame;

    switch(boss_mode) {
        // INTRO, SELECT, Orbit, Entities, Alternate, DESCEND, EXPLODE
    }

    boss_render_frame += boss_spin_delta;
    // collision map and hitbox/HP tail
}
```

The original mismatch early return is replaced by the positive scope. The
bullet-template PID assignment remains before the target update; the frame
increment precedes the mode switch; and the signed-byte spin update remains
a compound `+=` after the switch, before collision-map setup. The existing
comment records that spelling as codegen-sensitive. INTRO/EXPLODE returns,
all three attack-family dispatches and the collision/HP tail retain their
original order.

Stage `af1033e` rebuilt the complete `ba_rikak` physical owner in two
independent original TC4 4.02 rounds. All 1,677 CODE bytes, 215 ordered native
fields and eight PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1033e/report.json`

SHA-256: `f4c3a08dcd0d2c3691715c50928995baf01559f6ecd1a8f96023a18626b98650`
