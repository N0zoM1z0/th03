# TH03 MAIN Chiyuri + HitCircle integration after1028

The current Chiyuri BOSS and HitCircle collision sources were rebuilt
together as two complete physical MAIN owners in stage `af1028g`:

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

The integrated source changes are:

- Chiyuri's fan generator uses an explicit SI register index (af1027a).
- Chiyuri's large update controller has a complete explicit INTRO
  done/cross/default chain (af1027h), and a register-qualified byte selector
  in its SELECT center-array lookup (af1028f).
- HitCircle's update and render loops now express the original SI record
  pointers and AX/DI counters as register locals (af1027f/g, af1028c).
- HitCircle's render pass uses the positive active-record guard (af1028d).

Protected report: `.analysis/work/exatt-layout-af1028g/report.json`

SHA-256: `9873bccf30dd3073f5120db3cacfebabe06feeaf0be783d0996a089184966b63`
