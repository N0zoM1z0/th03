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
