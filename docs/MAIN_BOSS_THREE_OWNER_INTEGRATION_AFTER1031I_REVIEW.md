# TH03 MAIN Kotohime + Mima + Chiyuri integration after1031i

The current three BOSS sources were rebuilt together as complete physical MAIN
owners in stage `af1031i`:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_koto` | 1,840 | 262 | 11 |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_chiyu` | 2,654 | 381 | 11 |
| **Total** | **6,416** | **920** | **31** |

Two independent original Turbo C++ 4.02 rounds reproduced all three complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these three physical owners were rebuilt; unaffected original objects
and CRT were reused.

The integrated source includes the current Kotohime radial-burst nested
pre-tested `while` loops with register DI/SI indices and per-center scratch
lifetimes (af1031h), alongside the already maintained Kotohime update/Pellet,
Mima update/Orbit/Trail, and Chiyuri update/Cardinal/Rings/Trail/Fans work.

Protected report: `.analysis/work/exatt-layout-af1031i/report.json`

SHA-256: `b546fb907b8c9da943ebdfb0de7cc4c62ab46c9775bb606235370e4e8365c7d4`
