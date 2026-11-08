# TH03 MAIN current nine-BOSS integration after1038x

All nine current complete BOSS physical owners were rebuilt simultaneously
at stage `af1038x`, after the latest complete Chiyuri Update arithmetic and
local-lifetime refinements:

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

This integration includes the af1036 Mima/Yumemi work, af1037 Chiyuri Fans
and Kotohime Radial/Update work, and the af1038 Chiyuri Update work. No full
cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1038x/report.json`

SHA-256: `c7cbcc490d92d15bf8379c40a275e2d6af7b75324f149b7db36a9996d8dd8a9c`
