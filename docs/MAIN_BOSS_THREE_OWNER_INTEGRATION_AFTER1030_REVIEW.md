# TH03 MAIN Kotohime + Mima + Chiyuri integration after1030

The current Kotohime, Mima and Chiyuri BOSS sources were rebuilt together as
three complete physical MAIN owners in stage `af1030l`:

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

The current source changes include:

- Kotohime's 332-byte update controller uses a positive INTRO completion
  branch with an explicit `else return` (af1030m).
- Mima's 298-byte update controller uses the corresponding positive INTRO
  success branch (af1030f).
- Chiyuri's 613-byte update controller has the low-bit render cadence and
  direct byte-phase truth tests (af1030c/d/e).
- Chiyuri's 352-byte Cardinal, 208-byte Rings and 115-byte Trail leaves scope
  their emission paths under positive cadence/fire conditions, preserving
  warning, finish and projectile ordering (af1030h/i/j).

The attempted Mima speed-field deduplication was rejected: copying
`mima_bullet_speed` into `mima_random_speed` instead of re-evaluating the
level-plus-base expression reduced the object to 1,920 CODE bytes. The
original reload and add are retained.

Protected report: `.analysis/work/exatt-layout-af1030l/report.json`

SHA-256: `b444cb80319866c800983ba444ca724306c997269ac82d8080cf69dbdc3f3b6e`
