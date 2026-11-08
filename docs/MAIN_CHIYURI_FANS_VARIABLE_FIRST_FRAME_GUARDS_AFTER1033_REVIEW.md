# TH03 MAIN Chiyuri Fans: variable-first frame guards

The 528-byte `chiyuri_pattern_fans()` leaf now uses variable-first frame
comparisons for both independent firing phases:

```cpp
if(boss_frame == CHIYURI_FAN_HORIZONTAL_FRAME) {
    // horizontal warning, two mirrored shots and two speed passes
    return;
}

if(boss_frame == CHIYURI_FAN_VERTICAL_FRAME) {
    // vertical warning, fan shots and two speed passes
}
```

The horizontal branch still returns after its two distinct ascending and
descending passes. The vertical path remains an independent second test; its
warning pair, fan-angle calculations, ascending/descending speed updates and
final SELECT transition are unchanged.

A nearby natural unary-negation spelling was also tested:

```cpp
bullet_template.angle = -bullet_template.angle;
```

It changed complete `ba_chiyu` CODE and was reverted. Keep the exact
`(0 - bullet_template.angle)` spelling for the mirrored horizontal shot.

Stage `af1033q` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 4.02 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1033q/report.json`

SHA-256: `262f4bb195747fb72b2febf84a93c0ae4c1c9291743c4105d9e5a2c5140b3d45`
