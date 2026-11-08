# TH03 MAIN Yumemi Update: positive INTRO completion branch

The INTRO case in the complete Yumemi update controller now spells its
completion path as a positive equality branch after the two sound-frame
checks:

```cpp
if(boss_frame == YUMEMI_INTRO_FINISH_FRAME) {
    boss_frame = 0;
    boss_mode = YUMEMI_MODE_SELECT;
} else {
    return;
}
break;
```

The two earlier INTRO sound checks still run before this frame test, in their
original order. A non-completion frame still returns immediately; the
completion frame still resets the clock and enters SELECT before leaving the
switch. The active-player scope and all later mode dispatch/effect/collision
logic remain unchanged.

Stage `af1033j` rebuilt the complete `ba_yumem` physical owner in two
independent original TC4 4.02 rounds. All 2,358 CODE bytes, 343 ordered native
fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1033j/report.json`

SHA-256: `082168faca642419355286b3efac7508d3e4ddbb32327720a087cc9f2caf1eb4`
