# TH03 MAIN Mima + Chiyuri integration after1034u

The current complete Mima and Chiyuri physical owners were rebuilt together
at stage `af1034u` after the renderer and Fans refinements:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_chiyu` | 2,654 | 381 | 11 |
| **Total** | **4,576** | **658** | **20** |

Two independent original Turbo C++ 4.02 rounds reproduced both complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these two physical BOSS objects were rebuilt; unaffected original
objects and CRT were reused.

The integrated source includes Mima's positive Trail renderer guard,
constant-first Particle thresholds and variable-first mode checks, plus
Chiyuri's four ordered speed/index loop steps, named fan edge, base-first
coordinate arithmetic and constant-first span/angle products.

Protected report: `.analysis/work/exatt-layout-af1034u/report.json`

SHA-256: `97e45297142970a0defc3cba08e3a1053fec0ccebfea336d0e42f04b4d63587a`
