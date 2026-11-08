# TH03 MAIN current ten-owner integration after1044n

All nine complete BOSS physical owners and the complete four-function
HitCircle physical owner were rebuilt simultaneously at stage `af1044n` after
the Reimu Orbit Burst, Orbit Cloud and Update natural-C++ refinements:

| Owner | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_chiyu` | 2,654 | 381 | 11 |
| `ba_kana` | 1,874 | 274 | 9 |
| `ba_koto` | 1,840 | 262 | 11 |
| `ba_ellen` | 1,675 | 213 | 9 |
| `ba_rikak` | 1,677 | 215 | 8 |
| `ba_yumem` | 2,358 | 343 | 10 |
| `ba_mima` | 1,922 | 277 | 9 |
| `ba_reimu` | 2,020 | 270 | 9 |
| `ba_maris` | 1,431 | 199 | 9 |
| `hitcirc` | 445 | 30 | 4 |
| **Total** | **17,896** | **2,464** | **89** |

Two independent original Turbo C++ 4.02 rounds reproduced all ten complete
owners' CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only these ten physical owners were rebuilt; unaffected original game
objects and CRT were reused.

The Reimu changes in this integration cover its 443-byte Orbit Burst,
339-byte Orbit Cloud and 296-byte Update controller. The other nine physical
owners and HitCircle remain unchanged from the preceding af1042k integration.
No full cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1044n/report.json`

SHA-256: `4ce7bc32cccaf72452daa4546b2ac60cbd55dd9699fa948a2afc6f32618f5511`
