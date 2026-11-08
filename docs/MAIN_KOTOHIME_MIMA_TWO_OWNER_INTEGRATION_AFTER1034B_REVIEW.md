# TH03 MAIN Kotohime + Mima integration after1034b

The current Kotohime radial-burst and Mima Trail source refinements were
rebuilt together as two complete physical MAIN owners at stage `af1034b`:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_koto` | 1,840 | 262 | 11 |
| `ba_mima` | 1,922 | 277 | 9 |
| **Total** | **3,762** | **539** | **20** |

Two independent original Turbo C++ 4.02 rounds reproduced both complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these two physical BOSS objects were rebuilt; unaffected original
objects and CRT were reused.

The current source includes Kotohime's scoped natural `for` traversals,
positive release guard, named warning-radius increment, base-first center
angle and speed arithmetic; and Mima Trail's natural destination-byte
narrowing and named fixed speed offset.

Protected report: `.analysis/work/exatt-layout-af1034b/report.json`

SHA-256: `27ed5178f6c7d3bf74ac680f7b79299312e1fdefdbe64e902be3a9af8e261a15`
