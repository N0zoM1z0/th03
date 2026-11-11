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

## Current-source frame-gate confirmation (2026-11-11)

The live `chiyuri_pattern_fans()` uses a direct return at the end of the
horizontal `0x20` release, followed by a standalone positive `0x40` vertical
frame check. This retains the mutually exclusive volleys without an `else`
controlling the second phase. In native stage `af1349a`, both original TC4
rounds reproduce all 2,654 bytes of `ba_chiyu`, its 381 ordered fields,
11 PUBLICs, and the complete Japanese MAIN image and relocation sequence.
The checked proof is `.analysis/work/exatt-layout-af1349a/report.json`.

Two further natural-source experiments were rejected against the same whole
owner. Stage `af1349b` replaced the render-frame boolean accumulation with
an explicit `if`/byte increment (2,643 instead of 2,654 CODE bytes). Stage
`af1349c` replaced the intro's explicit AL-carried phase increments with a
`register unsigned char` local (2,669 CODE bytes). Both compiled, but
neither reproduced the native CODE. The maintained source retains the original
compiler-visible expressions for those operations.
