# TH03 MAIN Mima + Chiyuri integration after1029

The current Mima renderer and Chiyuri fan-loop sources were rebuilt together
as two complete physical MAIN owners in stage `af1029k`:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_chiyu` | 2,654 | 381 | 11 |
| **Total** | **4,576** | **658** | **20** |

Two independent original Turbo C++ 4.02 rounds reproduced both complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Unaffected original objects were reused; this was a scoped two-owner build,
not a full cold replay.

The integrated source changes are:

- Mima's 305-byte `mima_render_main()` uses independent early-return guards
  for hit, Particle, Expand, Flash and Trail modes. The shared Particle/Trail
  label and byte-frame postincrement remain unchanged (af1029g).
- Chiyuri's 528-byte fan generator retains its four independent horizontal
  and vertical passes but uses natural postfix `i++` in all four loop headers
  (af1029j).

Protected report: `.analysis/work/exatt-layout-af1029k/report.json`

SHA-256: `126ffbd30dbab1de5d7d464bb550da5ed2e6404247f65e93925498e435b0eb80`
