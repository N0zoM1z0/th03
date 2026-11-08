# TH03 MAIN Chiyuri Fans: speed/index loop steps and shared edge offset

The four distinct fan passes in the 528-byte `chiyuri_pattern_fans()` leaf
now advance their byte speed and signed loop index together in the `for`
iteration expression. For example, the horizontal ascending pass is:

```cpp
for(
    i = 0;
    i < chiyuri_fan_count;
    bullet_template.speed.v = bullet_template.speed.v + CHIYURI_FAN_SPEED_STEP, ++i
) {
    // position and angle
    bullets_add();
    bullet_template.angle = (0 - bullet_template.angle);
    bullets_add();
}
```

The speed update still occurs after every bullet emission and before the next
count test. The comma expression sequences the byte-speed assignment before
`++i`, preserving the original operation order. The descending pass uses the
corresponding subtraction. The two vertical passes retain their single-shot
emission, with the same ascending/descending speed progression. All four
passes remain separate and preserve the horizontal/vertical warning calls,
shot counts, angle arithmetic and final SELECT transition.

The shared `TO_SP(56)` fan-edge distance is now named
`CHIYURI_FAN_EDGE_OFFSET`. Both warning-bomb pairs and all four fan-coordinate
expressions use the same named offset. The signed 16-bit multiply/divide
still occurs before scaling to subpixels.

Stage `af1034p` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 4.02 rounds. All 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLIC offsets match. Both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1034p/report.json`

SHA-256: `780635fbf7a7f1b6a62347afff94a4a9d84837e9d26d02d641400324e17c8223`
