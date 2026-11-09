# TH03 MAIN Marisa Update: positive launched-player scope

The complete 269-byte `gba_boss_update_marisa()` controller now scopes its
active update under the positive launched-player predicate:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_other = (1 - pid_current);
    boss_target_update();
    ++boss_frame;

    switch(boss_mode) {
        // INTRO, SELECT, Spread, Wide, Ring, Narrow, DESCEND and EXPLODE
    }

    // collision map and hitbox/HP tail
}
```

The previous form returned immediately on a player mismatch, then ran the
mode switch and collision tail outside the guard. The positive scope makes
the complete active-player lifetime explicit; a mismatch reaches the
function's implicit return. The INTRO early return, EXPLODE early return,
all four attack-family dispatches and the collision/HP tail retain their
original order.

Stage `af1032v` rebuilt the complete `ba_maris` physical owner in two
independent original TC4 4.02 rounds. All 1,431 CODE bytes, 199 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1032v/report.json`

SHA-256: `fb6b6431d5e3265b8badc58e916e0aed497252548d47115192de5b46bb206a6b`


## Later current-source form (af1065a)

The positive launched-player scope above is now a historical source spelling.
The current `gba_boss_update_marisa()` controller uses a direct inactive-player
return before target tracking and frame advancement:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}
```

The six level-derived parameter assignments remain before the guard. For the
launched player, the INTRO/SELECT, Spread, Wide, Ring, Narrow, DESCEND and
EXPLODE dispatch stays in order, followed by the complete collision-map and
hitbox/HP tail.

Stage `af1065a` rebuilt the complete `ba_maris` physical owner in two
independent original TC4 4.02 rounds: all 1,431 CODE bytes, 199 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered relocations.

Current-source report: `.analysis/work/exatt-layout-af1065a/report.json`

SHA-256: `85c25305bb19ad8683e49d10c616d23de3d91abb57ca97e6c666b4afdb4f75b8`
