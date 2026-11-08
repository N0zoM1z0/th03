# TH03 MAIN current nine-BOSS integration after1033r

After the latest Chiyuri Fans source refinement, all nine complete BOSS
physical owners were rebuilt simultaneously again at stage `af1033r`:

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
| **Total** | **17,451** | **2,434** | **85** |

Two independent original Turbo C++ 4.02 rounds reproduced every complete
owner's CODE, ordered native fields and PUBLIC offsets. Both normal Japanese
MAIN links reproduced the original loaded image and ordered MZ relocations.
Only the nine physical BOSS objects were rebuilt; unaffected original objects
and CRT were reused.

This is the current integration of all nine positive launched-player scopes,
the positive INTRO completion branches and Chiyuri's variable-first Fans
frame guards. It supersedes the earlier nine-owner af1033o integration as the
current-source integration receipt.

Protected report: `.analysis/work/exatt-layout-af1033r/report.json`

SHA-256: `364eb749fea666529c45d0268c6d29ef1da3173c4da652ac5076cce6ccfcbdfc`
