# TH03 MAIN Chiyuri fan generator: four natural while passes (af1069u)

The complete 528-byte `chiyuri_pattern_fans()` producer now expresses all
four independent fan traversals as natural pre-tested `while` loops. The
shared signed index is initialized at each pass, and the byte-speed mutation
and prefix index increment are explicit at the end of each loop body.

The horizontal ascending pass is representative:

```cpp
i = 0;
while(i < chiyuri_fan_count) {
    // center, angle, original shot
    bullets_add();
    bullet_template.angle = (0 - bullet_template.angle);
    bullets_add();
    bullet_template.speed.v = CHIYURI_FAN_SPEED_STEP + bullet_template.speed.v;
    ++i;
}
```

The horizontal descending pass uses the original speed subtraction. The two
vertical passes use the same ascending/descending speed progression, with one
projectile emission per iteration. The horizontal mirrored-angle subtraction,
vertical angle calculation, signed multiply/divide-before-`TO_SP` coordinate
rounding, warning-bomb calls and final SELECT transition remain unchanged.

The order of operations is the important invariant: each iteration emits its
original projectile(s), then mutates the byte speed, then advances the signed
index. This is the same order previously expressed by the comma-separated
`for` iteration expression, but the `while` form makes the sequence visible
inside the body. Both postfix `i++` and prefix `++i` at the end of these while
bodies were independently tested; the maintained source uses prefix `++i`.

## Complete original-owner verification

Stage `af1069u` rebuilt the complete `ba_chiyu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLIC offsets match. Both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1069u/report.json`

SHA-256: `c4ac3dce799ad355973af2c11a9628b956da5150f0dcd10b5db8c332416152e3`

Source SHA-256: `0cb1fdc3c7a402df23540ceb3067b8513e057397e3cfe563c46d21c1f6ae2daa`

## Joint current-source integration

Stage `af1069v` rebuilt Yumemi and Chiyuri together in two independent
original TC4 rounds: 5,012 CODE bytes, 724 ordered native fields and 21 PUBLIC
offsets match. Both complete normal Japanese MAIN links reproduce the original
loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1069v/report.json`

SHA-256: `df1f19a221c9898b0ea988a73bb24f9503903fbdadb721c57069373b62ad8339`
