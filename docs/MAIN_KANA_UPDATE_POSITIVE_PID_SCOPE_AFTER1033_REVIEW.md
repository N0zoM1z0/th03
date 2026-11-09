# TH03 MAIN Kana Update: positive launched-player scope

The complete 316-byte `gba_boss_update_kana()` controller now scopes its
active path under the positive launched-player predicate:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_other = (1 - pid_current);
    bullet_template.pid = pid_other;
    boss_target_update();
    ++boss_frame;

    switch(boss_mode) {
        // INTRO, SELECT, Accel, Staged, Cloud, Rotating, DESCEND, EXPLODE
    }

    boss_render_frame++;
    // collision map and hitbox/HP tail
}
```

The original mismatch early return is replaced by the positive active-player
scope. The bullet-template PID assignment remains before the target update;
the BOSS frame increments before mode dispatch, while the render-frame
postfix increment remains after the switch and before collision-map setup.
The INTRO and EXPLODE early returns and all four attack-family dispatches
retain their original order.

Stage `af1033c` rebuilt the complete `ba_kana` physical owner in two
independent original TC4 4.02 rounds. All 1,874 CODE bytes, 274 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1033c/report.json`

SHA-256: `af0ae301ce8b189d9a5ff5bfdde470a23760af02968eed59489b06ef7b5983c3`


## Later current-source form (af1060a)

The positive launched-player scope above is now a historical source spelling.
The current `gba_boss_update_kana()` controller uses a direct inactive-player
return before bullet PID setup, target tracking and frame advancement:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}
```

The seven level-derived parameters remain initialized before this guard.
For the launched player, the INTRO/SELECT, Accel, Staged, Cloud, Rotating,
DESCEND and EXPLODE cases retain their order; the render-frame postfix and
collision/hitbox/HP tail remain after the switch.

Stage `af1060a` rebuilt the complete `ba_kana` physical owner in two
independent original TC4 4.02 rounds: all 1,874 CODE bytes, 274 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered relocations.

Current-source report: `.analysis/work/exatt-layout-af1060a/report.json`

SHA-256: `da7b824a76578facb835758886e2ca95e2a6d5788b5548b3b2084cfb59bb3d29`
