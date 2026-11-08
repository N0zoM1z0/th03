# TH03 MAIN current twelve-owner integration after1047l

After the shared BOSS ring and controller recovery, the two original shared
BOSS physical objects were rebuilt together with all nine complete character
BOSS owners and the complete four-function HitCircle owner at stage
`af1047l`:

| Physical object | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_sring` | 348 | 22 | 1 |
| `ba_srest` | 601 | 84 | 7 |
| `ba_chiyu` | 2,654 | 381 | 11 |
| `ba_kana` | 1,874 | 274 | 9 |
| `ba_koto` | 1,840 | 262 | 11 |
| `ba_ellen` | 1,675 | 213 | 9 |
| `ba_rikak` | 1,677 | 215 | 8 |
| `ba_yumem` | 2,358 | 343 | 10 |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_reimu` | 2,020 | 270 | 9 |
| `ba_maris` | 1,431 | 199 | 9 |
| `hitcirc` | 445 | 30 | 4 |
| **Total** | **18,845** | **2,570** | **97** |

Two independent original Turbo C++ 4.02 rounds reproduced all twelve
physical owners' CODE, ordered native fields and PUBLIC offsets. Both normal
Japanese MAIN links reproduced the original loaded image and ordered MZ
relocations. Only these twelve physical objects were rebuilt; the other 87
game objects and CRT were reused. No full cold replay was run.

This integration includes the shared ring's two natural `for` loops, register
byte angle, base-first sprite placement and explicit byte arithmetic; the
shared launch, movement, hit/death, target and pattern controllers' positive
guards and early returns; and the already-integrated nine BOSS/HitCircle
sources, including Reimu's three-phase Orbit Burst and Orbit Cloud recovery.

Protected report: `.analysis/work/exatt-layout-af1047l/report.json`

SHA-256: `3f0ce5c021307f20997ce97ad2d833cc8853722b7e4d9f37c19e1bad023db544`
