# TH03 MAIN BOSS integration after1026

The current Kotohime, Mima and Chiyuri source changes were rebuilt together
as three complete physical MAIN_03_TEXT owners in stage `af1026j`:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_koto` | 1,840 | 262 | 11 |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_chiyu` | 2,654 | 381 | 11 |
| **Total** | **6,416** | **920** | **31** |

Two independent original Turbo C++ 4.02 rounds reproduced every complete
owner's CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
The probe reused unaffected original objects; it was not a full cold replay.

The source-bound changes covered by this integration are:

- Kotohime's early-return inactive-PID controller guard and explicit
  `register int` outer/inner radial loop indices.
- Mima's constant-first inclusive finish comparisons in Orbit and Trail.
- Chiyuri's mutually exclusive intro-frame `if`/`else if` chain.

Protected report: `.analysis/work/exatt-layout-af1026j/report.json`

SHA-256: `bdd8fa9a8aa3937ca58dfdf97cf5d9ff43bc6c4c4a8bf9223ff6cd4cfccd7189`

This is current-source scoped native evidence, not canonical packed-file
Factory acceptance or whole-game source ownership.
