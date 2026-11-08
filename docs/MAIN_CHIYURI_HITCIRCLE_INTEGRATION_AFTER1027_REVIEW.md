# TH03 MAIN Chiyuri + HitCircle integration after1027

The current Chiyuri BOSS and HitCircle collision sources were rebuilt
simultaneously as two complete physical MAIN owners in stage `af1027i`:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_chiyu` | 2,654 | 381 | 11 |
| `hitcirc` | 445 | 30 | 4 |
| **Total** | **3,099** | **411** | **15** |

Two independent original Turbo C++ 4.02 rounds reproduced both complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Unaffected original objects were reused; this was a scoped two-owner build,
not a full cold replay.

The source changes integrated here are:

- Chiyuri's four-pass fan generator explicitly declares its shared SI loop
  index as `register int` (af1027a).
- Chiyuri's 613-byte update controller makes the INTRO default animation and
  return path the explicit final `else` of its done/cross/default frame chain
  (af1027h).
- HitCircle's 38-byte age update declares both the SI near-record cursor and
  AX signed loop counter as register locals (af1027f/g).

Protected report: `.analysis/work/exatt-layout-af1027i/report.json`

SHA-256: `81e18f4557ad5d302a988e501afc09416666b520f71a5d1c03fbbae84df268a0`

This is source-bound scoped native evidence, not canonical packed-file
Factory acceptance or whole-game source ownership.
