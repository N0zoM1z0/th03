# TH03 MAIN current nine-BOSS integration after1037t

All nine current complete BOSS physical owners were rebuilt simultaneously
again at stage `af1037t`, after the Chiyuri Fans subpixel/loop arithmetic,
Kotohime Radial scratch/arithmetic and Kotohime Update formula refinements:

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

This current integration includes the Mima and Yumemi source refinements
recorded at af1036u, plus the Chiyuri Fans and Kotohime Radial/Update work
recorded at af1037s. No full cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1037t/report.json`

SHA-256: `f83dc9dc84b591ce5bde63f76cbc4c08df23a3fba5d21cf821861ed23b16e1c5`
