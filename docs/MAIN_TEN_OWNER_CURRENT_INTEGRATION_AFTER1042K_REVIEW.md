# TH03 MAIN current ten-owner integration after1042k

All nine complete BOSS physical owners and the complete four-function
HitCircle physical owner were rebuilt simultaneously again at stage
`af1042k`, after the Chiyuri render-coordinate and Mima Trail/Orbit/Update
plus main/split-renderer refinements:

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
| `hitcirc` | 445 | 30 | 4 |
| **Total** | **17,896** | **2,464** | **89** |

Two independent original Turbo C++ 4.02 rounds reproduced all ten complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these ten physical owners were rebuilt; unaffected original game
objects and CRT were reused.

This current integration includes the Mima/Yumemi work through af1036,
Chiyuri Fans and Kotohime Radial/Update through af1037, Chiyuri Update through
af1038, HitCircle spawn through af1039, Chiyuri renderers and Mima
Trail/Orbit/Update through af1041, and Mima main/split renderers through
af1042. No full cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1042k/report.json`

SHA-256: `66d06f1182ee23c85b2a64184ca5d5defe9a1c732386ef2bb0266679971e2a25`
