# TH03 MAIN Chiyuri Update: named random-mode base

The SELECT timer transition in the 613-byte `gba_boss_update_chiyuri()` now
uses the first Cardinal mode as the random pattern range's base:

```cpp
boss_mode = (
    randring_far_next16_and(0x0F) + CHIYURI_MODE_CARDINAL_0
);
```

`CHIYURI_MODE_CARDINAL_0` is the original mode value `0x02`. Adding the
masked four-bit random value therefore still selects the contiguous mode
range `0x02..0x11` spanning Cardinal, Rings, Trail and Fans. The random call
is evaluated once, the result is stored before the pattern counter advances,
and the existing descent override remains last.

Stage `af1032f` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 4.02 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1032f/report.json`

SHA-256: `c961ad7674ed4c9c23df75a65bd492b78b7d5f8ff7e61c6ceb86423c1426dcc1`
