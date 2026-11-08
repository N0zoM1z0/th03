# TH03 MAIN Kotohime + Mima + Chiyuri integration after1030r

The current three BOSS sources were rebuilt together as complete physical MAIN
owners in stage `af1030r`:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_koto` | 1,840 | 262 | 11 |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_chiyu` | 2,654 | 381 | 11 |
| **Total** | **6,416** | **920** | **31** |

Two independent original Turbo C++ 4.02 rounds reproduced all three complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these three physical owners were rebuilt; all unaffected original
objects and CRT were reused.

This integrated revision includes:

- Kotohime's positive INTRO completion branch (af1030m).
- Mima's positive INTRO completion branch and variable-first orbit finish
  predicate (af1030f/af1030n).
- Chiyuri's update-controller cadence/phase cleanups, positive Cardinal,
  Rings and Trail guards, positive vertical Fans guard, and independent
  horizontal/vertical Fans frame tests (af1030c/d/e/h/i/j/p/q).

Protected report: `.analysis/work/exatt-layout-af1030r/report.json`

SHA-256: `e0b068741ed6bdd6822c82cdd9ab16957c557deb960778063c3d9f7bc4696de0`
