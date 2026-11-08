# TH03 MAIN Mima + Yumemi integration after1036t

The current complete Mima and Yumemi physical owners were rebuilt together
at stage `af1036t` after the Mima level/template/attack-clock changes and the
Yumemi update plus all five attack-pattern refinements:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_yumem` | 2,358 | 343 | 10 |
| **Total** | **4,280** | **620** | **19** |

Two independent original Turbo C++ 4.02 rounds reproduced both complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these two physical BOSS objects were rebuilt; unaffected original
objects and CRT were reused.

Protected report: `.analysis/work/exatt-layout-af1036t/report.json`

SHA-256: `bf867ed737a3d8ed74c7922f087389226683386db5dc0eb9fc10d69fb085b0bb`
