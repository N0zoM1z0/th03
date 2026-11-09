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


## Later current-source form (af1066a)

The positive launched-player scope above is now a historical source spelling.
The current `gba_boss_update_rikako()` controller uses a direct inactive-player
return before bullet PID setup, target tracking and frame advancement:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}
```

The five level-derived parameters remain before the guard. For the launched
player, the INTRO/SELECT, Orbit, Entities, Alternating Burst, DESCEND and
EXPLODE dispatch stays in order. The signed-byte spin compound update and the
complete collision/hitbox/HP tail remain after the switch.

Stage `af1066a` rebuilt the complete `ba_rikak` physical owner in two
independent original TC4 4.02 rounds: all 1,677 CODE bytes, 215 ordered native
fields and eight PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered relocations.

Current-source report: `.analysis/work/exatt-layout-af1066a/report.json`

SHA-256: `17e3ec6f9a147a36d35f77af3f6e73742efbe4605b7b9832f4773b6474fdc1b4`
