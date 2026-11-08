# TH03 MAIN Mima + Chiyuri integration after1030

The current Mima update-controller and Chiyuri update/attack-leaf changes were
rebuilt together as two complete physical MAIN owners in stage `af1030k`:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_chiyu` | 2,654 | 381 | 11 |
| **Total** | **4,576** | **658** | **20** |

Two independent original Turbo C++ 4.02 rounds reproduced both owners'
complete CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these two physical TUs were rebuilt; the other original objects and CRT
were reused.

The integrated source work includes:

- Mima's 298-byte update controller now uses a positive INTRO completion
  branch with an explicit non-completion `else return` (af1030f).
- Chiyuri's 613-byte update controller uses a four-frame low-bit cadence
  test, direct byte truth tests for the render/palette countdowns, and the
  zero-valued render-mode truth test (af1030c/d/e).
- Chiyuri's 352-byte Cardinal, 208-byte Rings and 115-byte Trail leaves now
  express their firing paths as positive conditions while preserving their
  separate setup, finish, warning and projectile ordering (af1030h/i/j).

A tempting Mima update deduplication was rejected: replacing the second
`gba_boss_level + MIMA_LEVEL_BULLET_BASE` expression with a copy of
`mima_bullet_speed` reduced the owner from 1,922 to 1,920 CODE bytes. The
original deliberately reloads the level byte and adds the base again for
`mima_random_speed`; keep both source expressions separate.

Protected report: `.analysis/work/exatt-layout-af1030k/report.json`

SHA-256: `c4689d787956b37fd8c9fa1071960d53b431d8b180384a912fbed305ac53f469`
