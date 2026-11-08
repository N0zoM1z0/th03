# TH03 MAIN Chiyuri Fans: TO_SP scaling, center offsets and loop steps

The four distinct 528-byte fan passes now express their signed coordinate
scaling through the shared `TO_SP` macro, keeping the integer division before
subpixel conversion:

```cpp
TO_SP((CHIYURI_FAN_SPAN_PIXELS * i) / chiyuri_fan_count)
```

This is not a quotient rewrite: the signed 16-bit `(span * i) / count`
calculation completes before `TO_SP` scales the resulting pixel displacement.
The obsolete local `CHIYURI_FAN_SPAN_TO_SUBPIXELS` constant was removed.

All four fan-center expressions also use an exact edge-first grouping:

```cpp
(boss_center_x - CHIYURI_FAN_EDGE_OFFSET) +
    TO_SP((CHIYURI_FAN_SPAN_PIXELS * i) / chiyuri_fan_count)
```

The vertical expressions use the corresponding Y center. Reordering the
center/edge arithmetic this way still reproduces the original TC4 instructions
and preserves the signed division-before-scaling result.

The two ascending speed passes now use constant-first addition:

```cpp
bullet_template.speed.v =
    CHIYURI_FAN_SPEED_STEP + bullet_template.speed.v;
```

All four `for` iteration expressions use postfix `i++` after the speed
assignment. The comma-expression order remains speed first, index second;
the four independent pass bodies, shot count, mirrored horizontal angle,
vertical angle and `bullets_add()` order are unchanged. Compound `+=`/`-=`
remains non-exact as recorded in the prior Fans reviews.

Stage `af1037q` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 4.02 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1037q/report.json`

SHA-256: `5c53fdc3597296a602a90b33b54ee82c007aadd8e1776ae28612719046f51985`
