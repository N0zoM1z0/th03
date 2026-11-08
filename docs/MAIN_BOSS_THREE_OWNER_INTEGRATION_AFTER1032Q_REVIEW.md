# TH03 MAIN Kotohime + Mima + Chiyuri integration after1032q

The current three BOSS update controllers were rebuilt together as complete
physical MAIN owners in stage `af1032q`:

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

The integrated update-controller work includes:

- Kotohime's 332-byte update controller now scopes the mode switch and
  collision/hitbox tail under the positive launched-player test
  (af1032p).
- Mima's 298-byte update controller uses the same positive active-player
  scope while retaining its deliberate post-target-update PID recomputation
  (af1032o).
- Chiyuri's 613-byte update controller scopes its complete active-player
  path under the positive predicate and retains its 20-mode dispatch and
  collision/hitbox tail (af1032l). Its SELECT path also uses explicit
  paired-center index scaling, a variable-first timer/palette guard and a
  named random-mode base (af1032b/c/e/f).

Protected report: `.analysis/work/exatt-layout-af1032q/report.json`

SHA-256: `260e2c05064b37975b5c4555d2146e00c2f9e09c8dfca58eb222c5a01747b031`
