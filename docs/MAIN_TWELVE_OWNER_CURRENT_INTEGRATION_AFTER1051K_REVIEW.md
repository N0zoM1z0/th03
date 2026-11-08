# TH03 MAIN current twelve-owner integration after1051k

After the latest Yumemi arrival, update-controller and main-renderer source
recovery, the two shared BOSS physical objects were rebuilt with all nine
complete character BOSS owners and the complete four-function HitCircle owner
at stage `af1051k`:

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

The new Yumemi changes cover the complete 368-byte update controller, the
333-byte main renderer, the 404-byte arrival raster and the 83-byte render
caller. The shared BOSS ring and launch/movement/hit/target/pattern controllers
remain integrated byte-exact alongside all nine character BOSS owners and
HitCircle.

Protected report: `.analysis/work/exatt-layout-af1051k/report.json`

SHA-256: `f1a95695b6eadcf3a91ad75d972cdf7f3fedef878cb3ca6ffa3ee7117ae871f1`
