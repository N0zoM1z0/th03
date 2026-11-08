# TH03 MAIN Kotohime + Mima + Chiyuri integration after1030u

The current three BOSS sources were rebuilt together as complete physical MAIN
owners in stage `af1030u`:

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

The integrated current source includes:

- Kotohime's positive INTRO completion branch (af1030m).
- Mima's positive INTRO completion branch and variable-first orbit finish
  predicate (af1030f/af1030n).
- Chiyuri's update-controller cadence/phase cleanups; positive Cardinal,
  Rings and Trail firing scopes; positive/independent Fans frame tests; and
  variable-first Cardinal/Rings finish predicates
  (af1030c/d/e/h/i/j/p/q/s/t).

Protected report: `.analysis/work/exatt-layout-af1030u/report.json`

SHA-256: `972457ab5c2f2cfce9beec4ed08dd727829d84ee443c0923e5a36c5503c65da8`
