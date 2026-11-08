# TH03 MAIN Chiyuri Fans: independent vertical test after horizontal return

The 528-byte `chiyuri_pattern_fans()` leaf now has two independent positive
frame tests:

```cpp
if(CHIYURI_FAN_HORIZONTAL_FRAME == boss_frame) {
    // horizontal warning and two speed passes
    return;
}

if(CHIYURI_FAN_VERTICAL_FRAME == boss_frame) {
    // vertical warning and two speed passes
}
```

The horizontal branch returns after its own pair of fan passes, so the
vertical test does not need to be written as an `else if`. The two firing
frames remain distinct; all warning, speed, angle, projectile and final
SELECT operations remain in their original order.

Stage `af1030q` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030q/report.json`

SHA-256: `05cf5f4971fbde85ff575000a15ce6846cbc848d9e6459e0c69c8902d6e6af5c`
