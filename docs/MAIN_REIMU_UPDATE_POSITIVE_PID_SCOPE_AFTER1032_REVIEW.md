# TH03 MAIN Reimu Update: positive launched-player scope

The complete Reimu BOSS update controller now scopes its active path under a
positive launched-player predicate:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_other = (1 - pid_current);
    boss_target_update();
    ++boss_frame;

    // INTRO/SELECT and the Cloud, Spread, Orbit Burst and Mirror dispatch
    // followed by the shared collision/hitbox tail
}
```

The former form returned immediately on a player mismatch and ran the full
mode dispatch/collision tail outside the guard. The positive scope keeps the
complete controller body together; the mismatch now reaches the implicit
return. The separate INTRO completion and EXPLODE returns, the pre-switch
SELECT handling, all four attack-family dispatches and the collision/HP tail
retain their original order.

Stage `af1032r` rebuilt the complete `ba_reimu` physical owner in two
independent original TC4 4.02 rounds. All 2,020 CODE bytes, 270 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1032r/report.json`

SHA-256: `e0f4198f2d80c4adb554bdd949a49b2c443bccfa1dd5fca5eaa7770e2582e433`
