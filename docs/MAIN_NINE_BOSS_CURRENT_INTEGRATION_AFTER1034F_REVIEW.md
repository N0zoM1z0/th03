# TH03 MAIN current nine-BOSS integration after1034f

The current nine complete BOSS physical owners were rebuilt simultaneously
again at stage `af1034f`, after the Kotohime Radial Burst and Mima Trail
source refinements:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_chiyu` | 2,654 | 381 | 11 |
| `ba_kana` | 1,874 | 274 | 9 |
| `ba_koto` | 1,840 | 262 | 11 |
| `ba_ellen` | 1,675 | 213 | 9 |
| `ba_rikak` | 1,677 | 215 | 8 |
| `ba_yumem` | 2,358 | 343 | 10 |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_reimu` | 2,020 | 270 | 9 |
| `ba_maris` | 1,431 | 199 | 9 |
| **Total** | **17,451** | **2,434** | **85** |

Two independent original Turbo C++ 4.02 rounds reproduced all nine complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only the nine physical BOSS objects were rebuilt; unaffected original objects
and CRT were reused.

The integrated source includes all nine positive launched-player scopes and
INTRO completion branches, Chiyuri's current Fans guard spelling, Kotohime's
natural Radial Burst traversal and Mima's Trail narrowing/speed cleanup.

Protected report: `.analysis/work/exatt-layout-af1034f/report.json`

SHA-256: `63520d8b5ffcac6c20c20f8748620aa666bed66b75cd5b35facc14aacd72140f`
