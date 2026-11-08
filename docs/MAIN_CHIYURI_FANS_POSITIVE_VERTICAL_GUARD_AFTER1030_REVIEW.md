# TH03 MAIN Chiyuri Fans: positive vertical-frame guard

The 528-byte `chiyuri_pattern_fans()` leaf now expresses the vertical fan path
as a positive condition:

```cpp
if(CHIYURI_FAN_VERTICAL_FRAME == boss_frame) {
    // vertical warning pair, ascending fan and descending fan
}
```

The horizontal path remains its own positive `if` and returns after its two
speed passes. The vertical path no longer needs an inverse-frame early return;
its two warning bombs, two projectile-speed passes, angle formula and final
SELECT transition are unchanged.

Stage `af1030p` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030p/report.json`

SHA-256: `bd470a2e8028e6f7900b73e58cd65e4fa18a9859499e5732259c11fc7de11729`
