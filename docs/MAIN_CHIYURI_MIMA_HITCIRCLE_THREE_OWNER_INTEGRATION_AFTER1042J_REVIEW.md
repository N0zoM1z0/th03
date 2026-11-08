# TH03 MAIN Chiyuri + Mima + HitCircle integration after1042j

The current complete Chiyuri and Mima BOSS owners plus the complete
four-function HitCircle physical owner were rebuilt simultaneously at stage
`af1042j` after the Chiyuri render-coordinate, Mima Trail/Orbit/Update and
Mima main/split-renderer source refinements:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_chiyu` | 2,654 | 381 | 11 |
| `ba_mima` | 1,922 | 277 | 9 |
| `hitcirc` | 445 | 30 | 4 |
| **Total** | **5,021** | **688** | **24** |

Two independent original Turbo C++ 4.02 rounds reproduced all three complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these three physical owners were rebuilt; unaffected original game
objects and CRT were reused.

This integration combines the complete Chiyuri render/update/Fans source
refinements, Mima's full update and attack-pattern work plus both major render
leaves, and the HitCircle spawn pointer/coordinate recovery. No full cold
replay was run.

Protected report: `.analysis/work/exatt-layout-af1042j/report.json`

SHA-256: `4351af381e039f0d52693761f4978ab0db066f978dbfe565e06f7ff0f5908a0d`
