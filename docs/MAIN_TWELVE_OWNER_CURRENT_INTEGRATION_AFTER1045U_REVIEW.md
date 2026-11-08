# TH03 MAIN current twelve-owner integration after1045u

The two original shared BOSS physical objects were integrated with all nine
complete BOSS owners and the complete four-function HitCircle owner, then
rebuilt together at stage `af1045u`:

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
relocations. Only these twelve physical objects were rebuilt; unaffected
original game objects and CRT were reused. No full cold replay was run.

This integration includes the Reimu Orbit Burst/Cloud/Update source recovery
from af1044 and the shared `boss_explosion_ring()` loop, coordinate and
arithmetic refinements from af1045. The `ba_srest` shared controller and the
other nine BOSS/HitCircle objects remain byte-exact.

Protected report: `.analysis/work/exatt-layout-af1045u/report.json`

SHA-256: `ecbc89e06242622c5397d7148dff12d623682ded2200e88bbc8b0cb7ce5413fe`
