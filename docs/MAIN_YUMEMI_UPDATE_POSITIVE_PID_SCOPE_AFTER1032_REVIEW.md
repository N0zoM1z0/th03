# TH03 MAIN Yumemi Update: positive launched-player scope

The complete 368-byte `gba_boss_update_yumemi()` controller now scopes its
active update under the positive launched-player predicate:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_other = (1 - pid_current);
    bullet_template.pid = pid_other;
    boss_target_update();
    ++boss_frame;

    yumemi_origin_x = boss_center_x + YUMEMI_ORIGIN_X_OFFSET;
    yumemi_origin_y = boss_center_y - YUMEMI_ORIGIN_Y_OFFSET;

    switch(boss_mode) {
        // INTRO, SELECT, Ring, Aimed, Cross, Chase, Rain, DESCEND, EXPLODE
    }

    // effect/render countdowns and collision/hitbox tail
}
```

The original PID-mismatch early return is replaced by the positive scope. The
bullet-template PID assignment remains before `boss_target_update()` (unlike
Mima's deliberately recomputed post-helper assignment), and both Yumemi
origin-coordinate calculations remain after the frame increment and before
the mode switch. The INTRO sound-frame checks, INTRO early return, EXPLODE
early return, five attack-family dispatches, effect-radius decay, postfix
render-frame decrement and collision/HP tail retain their original order.

Stage `af1032x` rebuilt the complete `ba_yumem` physical owner in two
independent original TC4 4.02 rounds. All 2,358 CODE bytes, 343 ordered native
fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1032x/report.json`

SHA-256: `02b2f3d29c4f2a23b22f1599692daf6eff802c2c9543ecabc18eca4d30efc9b3`
