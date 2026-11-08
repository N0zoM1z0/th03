# TH03 MAIN current twelve-owner integration after1053i

After the latest Yumemi ring, aimed, chase and rain cadence refinements, the
two shared BOSS physical objects were rebuilt with all nine complete
character BOSS owners and the complete four-function HitCircle owner at stage
`af1053i`:

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

This integration includes Yumemi's update controller, main and arrival
renderers, cross-ring producer, and natural modulo/phase tests for ring,
aimed, chase and rain attacks. The shared BOSS controllers/ring, all other
eight character BOSS owners and HitCircle remain exact in the same build.

Protected report: `.analysis/work/exatt-layout-af1053i/report.json`

SHA-256: `96dcbce66275423979c154779e690e540a96df6596be0d6fdbae3f08370dd254`
