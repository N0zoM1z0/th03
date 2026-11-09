# TH03 MAIN Mima Update: positive launched-player scope

The complete 298-byte `gba_boss_update_mima()` controller now scopes its
active update under the positive launched-player predicate:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_other = (1 - pid_current);
    boss_target_update();
    bullet_template.pid = (1 - pid_current);
    ++boss_frame;

    switch(boss_mode) {
        // INTRO, SELECT, Spread, Random, Trail, Orbit, DESCEND and EXPLODE
    }

    // collision map and hitbox/HP tail
}
```

Previously the controller returned immediately when the current player did
not match `gba_boss_launched_by`, then executed the complete switch and
collision tail outside that guard. The positive scope makes the active-player
lifetime explicit; the mismatch now reaches the implicit function return.
The deliberate recomputation of `bullet_template.pid` after
`boss_target_update()` remains unchanged, as do the INTRO/EXPLODE early
returns and every mode-dispatch/collision operation.

Stage `af1032o` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 4.02 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1032o/report.json`

SHA-256: `870867ca5523b4d99c20ebf1df991ba5917d41f044db2a82244dfa619f217314`


## Later current-source form (af1059a)

The positive launched-player scope above is now a historical source spelling.
The current `gba_boss_update_mima()` controller uses a direct inactive-player
return before target tracking and frame advancement:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}
```

The seven level-derived parameter initializations remain before this guard.
For the launched player, the existing INTRO/SELECT, Spread, Random, Trail,
Orbit, DESCEND and EXPLODE dispatch stays in order, followed by the original
collision-map and hitbox/HP tail. In particular, the bullet PID intentionally
recomputes `(1 - pid_current)` rather than reusing `pid_other`.

Stage `af1059a` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 4.02 rounds: all 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the loaded image and ordered relocations.

Current-source report: `.analysis/work/exatt-layout-af1059a/report.json`

SHA-256: `397144dec5bda10fd68ba3740c4409cd1adb38073fe30b2605235599d009f0a7`
