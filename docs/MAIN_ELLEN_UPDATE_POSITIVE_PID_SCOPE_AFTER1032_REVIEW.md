# TH03 MAIN Ellen Update: positive launched-player scope

The complete 269-byte `gba_boss_update_ellen()` controller now scopes its
active path under the positive launched-player predicate:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_other = (1 - pid_current);
    boss_target_update();
    boss_render_frame++;
    ++boss_frame;

    switch(boss_mode) {
        // INTRO, SELECT, Spread, Extra, Pellets, DESCEND and EXPLODE
    }

    // collision map and hitbox/HP tail
}
```

The prior mismatch early return is replaced with a positive scope. The
render-frame postfix increment remains before the 16-bit BOSS frame increment;
INTRO and EXPLODE still return from the function at their original points,
and Spread/Extra/Pellets dispatch and the collision tail remain ordered as
before.

Stage `af1032z` rebuilt the complete `ba_ellen` physical owner in two
independent original TC4 4.02 rounds. All 1,675 CODE bytes, 213 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1032z/report.json`

SHA-256: `c0bc7833288ada4525113593172aa43aecba1a44602bf2556684503d85b7959a`
