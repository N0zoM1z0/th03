# TH03 MAIN four-owner BOSS integration after1032t

The current Reimu, Kotohime, Mima and Chiyuri BOSS owners were rebuilt
simultaneously as four complete physical MAIN owners in stage `af1032t`:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_reimu` | 2,020 | 270 | 9 |
| `ba_koto` | 1,840 | 262 | 11 |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_chiyu` | 2,654 | 381 | 11 |
| **Total** | **8,436** | **1,190** | **40** |

Two independent original Turbo C++ 4.02 rounds reproduced all four complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these four physical owners were rebuilt; unaffected original objects
and CRT were reused.

All four current update controllers now use a positive launched-player scope
for their active work:

- Reimu's 2020-byte update controller keeps INTRO/SELECT, four attack-family
  dispatches and collision/hitbox work inside the active-player block
  (af1032r).
- Kotohime's 332-byte update controller keeps its mode dispatch and collision
  tail inside the block (af1032p).
- Mima's 298-byte update controller keeps its mode dispatch and collision
  tail inside the block, including its deliberate recomputation of the
  bullet PID after `boss_target_update()` (af1032o).
- Chiyuri's 613-byte update controller keeps its 20-mode dispatch, render and
  palette countdowns, and collision/hitbox tail inside the block (af1032l).

The Chiyuri SELECT index/timer/palette/mode-base refinements are also present
in this integrated revision (af1032b/c/e/f).

Protected report: `.analysis/work/exatt-layout-af1032t/report.json`

SHA-256: `9355726ffe041293b933672f7240d401ad24fbab83d0c7917554ce0820b8afd8`
