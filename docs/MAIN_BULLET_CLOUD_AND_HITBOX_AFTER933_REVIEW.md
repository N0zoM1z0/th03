# TH03 MAIN Bullet update: cloud cadence and direct collision coordinates

Inside the large, complete `bullets_update()` loop, the original cloud
cel-advance mask is now identified as a four-frame byte-age cadence.
The original `_AL = age & mask` and `FLAGS_ZERO` relationship is retained
because TC4 does not emit the same object from apparently equivalent C++
conditions: the direct `if((age & 3) == 0)` trial `af933a` shortened the
physical bullet CODE by one byte (2,684 instead of 2,685); the `if(!_AL)`
trial `af933b` lengthened it by two bytes (2,687).

The 12-pixel pellet/explosion hitbox update now directly uses the existing
C++ `coord_next` for its Y-coordinate arithmetic, rather than the `coord_y`
macro alias. The alias had disguised a redundant `coord_next = coord_next`
self-assignment. Removing that self-assignment in `af933d` retained the
original instructions; no assembly pad or invented register action is needed.
The original hitbox rectangle, hardware collision calls, and byte flags
remain unchanged.

`af933d` twice recompiled the **entire original physical Bullet engine**, not
just this collision block: 2,685 CODE bytes, 196 literal ordered native
OMF fixup fields, 20 PUBLICs and the original 9,500-byte BSS. Both normal
complete MAIN TLINK rounds reproduced the Japanese 124,642-byte loaded image
and its 1,553 ordered MZ relocations with the other 98 original game
objects and CRT reused. No cold replay. Native report:
`.analysis/work/exatt-layout-af933d/report.json`, SHA-256
`6d3336d0d649776de454087fc23f38045f2e1b5409d6aeea676cbbc3c81c889b`.

This improves natural source representation of historically covered CODE;
it is not new distinct game-byte or canonical Factory acceptance.
