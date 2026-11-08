# TH03 MAIN Chiyuri update controller: explicit intro default branch

The INTRO case in the 613-byte `gba_boss_update_chiyuri()` controller now
expresses all three mutually exclusive frame outcomes as one complete chain:

```cpp
if(boss_frame == CHIYURI_INTRO_DONE_FRAME) {
    // enter selection and initialize the palette cycle
    break;
} else if(boss_frame == CHIYURI_INTRO_CROSS_EFFECT_FRAME) {
    // spawn four cross-effect bombs in their original order
    break;
} else {
    bullet_template.is_animated = true;
    return;
}
```

Previously the default animation/return path followed the two branches as
unconditional fallthrough code; both explicit branches already left the
switch with `break`. Moving the default path into the final `else` makes the
frame partition explicit without changing any frame comparison, bomb order,
animation flag or switch exit.

Stage `af1027h` rebuilt the complete `ba_chiyu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLIC offsets match. Both normal MAIN links
reproduce the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1027h/report.json`

SHA-256: `7b17f534043906c66d28e0dcd56308538a897f7bf0e2600113d979d404b63605`
