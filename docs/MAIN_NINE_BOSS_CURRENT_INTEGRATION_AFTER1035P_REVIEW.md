# TH03 MAIN current nine-BOSS integration after1035p

All nine current complete BOSS physical owners were rebuilt simultaneously
again at stage `af1035p`, after the Mima split renderer, top-level render
dispatch, update controller and Random Bomb refinements:

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

The integrated Mima source now includes the positive launched-player render
scope, constant-first render mode tests, compound split-angle update,
postfix BOSS frame increment, constant-first INTRO completion, and
constant-first Random Bomb warning/fire/wait/ring/end comparisons. All other
eight BOSS owners remain integrated at their current source.

Protected report: `.analysis/work/exatt-layout-af1035p/report.json`

SHA-256: `9b8fbfbd73800b90e018658c471a0a42839a9c8a803eb008c28132b0001abe45`
