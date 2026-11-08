# TH03 MAIN Kotohime + Mima + Chiyuri integration after1029

The current Kotohime radial-index, Mima renderer and Chiyuri fan-loop sources
were rebuilt together as three complete physical MAIN owners in stage
`af1029m`:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_koto` | 1,840 | 262 | 11 |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_chiyu` | 2,654 | 381 | 11 |
| **Total** | **6,416** | **920** | **31** |

Two independent original Turbo C++ 4.02 rounds reproduced all three complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Unaffected original objects were reused; this was a scoped three-owner build,
not a full cold replay.

The integrated source changes are:

- Kotohime's radial attack declares its outer `center_i` register before the
  inner `bullet_i` register, retaining the original DI/SI allocation
  (af1029l).
- Mima's 305-byte main renderer uses independent early-return phase guards
  while preserving its shared Particle/Trail label (af1029g).
- Chiyuri's four fan loops use natural postfix `i++` headers without merging
  their distinct horizontal/vertical and ascending/descending passes
  (af1029j).

Protected report: `.analysis/work/exatt-layout-af1029m/report.json`

SHA-256: `936d725eb366ec059049eec0e95e0fb08544fe7aff3aefecf5cba1caacabdbea`
