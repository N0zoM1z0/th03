# TH03 MAIN Chiyuri Update: positive launched-player scope

The complete 613-byte `gba_boss_update_chiyuri()` controller now scopes its
active update under the positive launched-player predicate:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_other = (1 - pid_current);
    boss_target_update();
    bullet_template.is_animated = false;
    bullet_template.pid = pid_other;
    ++boss_frame;

    switch(boss_mode) {
        // INTRO, SELECT, four attack families, DESCEND and EXPLODE
    }

    // render cadence, palette countdown, collision map and hitbox tail
}
```

Previously the function returned immediately when the current player did not
match `gba_boss_launched_by`, then ran the entire controller and collision
tail unconditionally. The positive scope expresses the active player path as
a single block and lets the mismatch fall through to the function's implicit
return. The order of target update, animation flag/PID setup, 16-bit frame
increment, 20-mode switch dispatch, render/palette countdown, collision-map
setup and hitbox/HP tail remains unchanged.

This was verified on the complete physical owner, not a sliced controller.
Stage `af1032l` rebuilt `ba_chiyu` in two independent original TC4 4.02
rounds. All 2,654 CODE bytes, 381 ordered native fields and eleven PUBLIC
offsets match. Both normal Japanese MAIN links reproduce the original loaded
image and ordered MZ relocations.

Several tempting neighboring rewrites were rejected and restored during the
same exploration: caching all seven level-derived parameters in one local
byte; replacing the postfix byte pattern counter with prefix, assignment or
compound increment; replacing the signed integer `/ 2` or `/ 4` calculations
with shifts; and spelling `level * 2` as `level + level`. Each changed the
complete `ba_chiyu` CODE. Keep the direct level reads, postfix counter and
original division/multiply expressions.

Protected report: `.analysis/work/exatt-layout-af1032l/report.json`

SHA-256: `20019dc403da06fe0127c0aaac265814cc04ab7ecd74dffdd0c245717d6e6fbc`


## Later current-source form (af1058a)

The positive launched-player scope above is now a historical source spelling.
The current complete `gba_boss_update_chiyuri()` controller uses the direct
inactive-player return before target tracking, bullet-template PID setup and
frame advancement:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}
```

This was re-tested after the later natural level arithmetic, SELECT indexing,
INTRO cross-effect coordinates, frame cadence, palette countdown and full
Cardinal/Rings/Trail/Fans dispatch changes. The switch, animation restoration,
palette countdown and collision/hitbox tail remain in their original order.

Stage `af1058a` rebuilt the complete `ba_chiyu` owner in two independent
original TC4 4.02 rounds: all 2,654 CODE bytes, 381 ordered native fields and
eleven PUBLIC offsets match. Both complete normal MAIN links reproduce the
Japanese loaded image and ordered relocations.

Current-source report: `.analysis/work/exatt-layout-af1058a/report.json`

SHA-256: `dde32e0ba6923503b17958abcc9524f64c30f6e3918c552fc72e30edb384d970`
