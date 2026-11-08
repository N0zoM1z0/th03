# TH03 MAIN Kotohime + Mima + Chiyuri integration after1031t

The current three BOSS sources were rebuilt together as complete physical MAIN
owners in stage `af1031t`:

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

This integrated source includes:

- Kotohime's Radial Burst nested pre-tested `while` loops, register DI/SI
  indices and per-center scratch scopes (af1031h).
- Mima's Spread positive fire-window guard and Random Bomb positive post-
  warning wait-window guard (af1031m/af1031s).
- The previously maintained Kotohime/Mima/Chiyuri INTRO, update-controller,
  attack-leaf, finish-predicate and fan-loop changes.

Protected report: `.analysis/work/exatt-layout-af1031t/report.json`

SHA-256: `cbf33da0efc506398511a825efffbf41f5201d41070102b78a0be9276890104f`
