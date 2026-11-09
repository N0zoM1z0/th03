# TH03 reconstruction progress

All counts describe repository-local tracked scopes. The whole-game completion percentage is unknown.

| Product | Source-present / tracked extents | Current accepted scope | Stored target bytes |
| --- | ---: | --- | ---: |
| th03-op | 61/62 | Decoded: 60 extents / 14,985 bytes | 36,041 |
| th03-main | 106/106 | Ledger: 106 extents / 78,737 bytes | 130,882 |
| th03-mainl | 259/259 | Decoded: 220 extents / 37,968 bytes | 37,975 |
| th03-zun | 77/78 | Decoded: 77 extents / 8,635 bytes | 16,242 |

Source-present means a maintained source path exists; it does not grant exact acceptance. Tracked extents can be functions, modules or DATA owners. All chart bars use these extents. Unaccepted inventory rows can contain finer accepted scopes, so their count is not a count of missing functions.

MAIN's separate function ledger records 459/459 exact entries. The other products have no equivalent function ledger; a zero function count would be misleading. Ledger acceptance is distinct from revalidation against current source; selected current native reviews follow below.

Stored target sizes are original file sizes, including DIET packing for OP/MAINL/ZUN. They are not decoded CODE denominators. OP/MAINL/ZUN canonical packed-unit credit remains zero; that does not erase decoded or scoped native work.

## Current source-native reviews

These read-only checks validate maintained source bindings, both original compiler rounds, complete physical owners, ordered native fields and normal target-equal links. Other link inputs are reused; these results do not grant broad decoded publication or whole-product ownership.

| Product / scope | Stage | Current check | Physical owners | CODE bytes | Initialized DATA bytes |
| --- | --- | --- | ---: | ---: | ---: |
| th03-main / Shared BOSS | af1109c | Verified | 2 | 949 | — |
| th03-main / Ellen Extra Attack | af1129e | Verified | 1 | 1,129 | — |
| th03-main / Yumemi Extra Attack | af1127g | Verified | 1 | 1,696 | — |
| th03-main / Mima Extra Attack | af1128c | Verified | 1 | 727 | — |
| th03-main / Reimu Extra Attack | af1112h | Verified | 2 | 1,156 | — |
| th03-main / Marisa Extra Attack | af1113c | Verified | 1 | 676 | — |
| th03-main / Kotohime Extra Attack | af1121d | Verified | 1 | 1,054 | — |
| th03-main / Chiyuri Extra Attack | af1122c | Verified | 1 | 978 | — |
| th03-main / Rikako Extra Attack | af1124d | Verified | 1 | 702 | — |
| th03-main / Kana Extra Attack | af1125e | Verified | 1 | 663 | — |
| th03-main / Rikako BOSS | af1118e | Verified | 1 | 1,677 | — |
| th03-main / Kana BOSS | af1117f | Verified | 1 | 1,874 | — |
| th03-main / Chiyuri BOSS | af1119b | Verified | 1 | 2,654 | — |
| th03-main / Kotohime BOSS | af1123e | Verified | 1 | 1,840 | — |
| th03-main / Reimu BOSS | af1104e | Verified | 1 | 2,020 | — |
| th03-main / Mima BOSS | af1105d | Verified | 1 | 1,922 | — |
| th03-main / Marisa BOSS | af1110d | Verified | 1 | 1,431 | — |
| th03-main / Ellen BOSS | af1111e | Verified | 1 | 1,675 | — |
| th03-main / Yumemi BOSS | af1130c | Verified | 1 | 2,358 | — |
| th03-main / Bullet engine | af1107c | Verified | 1 | 2,685 | — |
| th03-main / Fireball engine | af1108e | Verified | 1 | 1,555 | — |
| th03-main / Enemy engine | af1114e | Verified | 4 | 3,325 | — |
| th03-main / Explosion collision | af1120c | Verified | 1 | 630 | — |
| th03-main / Hitbox and HitCircle | af1101g | Verified | 2 | 711 | — |
| th03-main / Background chains | af1115b | Verified | 2 | 1,245 | — |
| th03-main / MAIN entry and round | af1126c | Verified | 1 | 3,050 | — |
| th03-main / Player core | af1116g | Verified | 1 | 3,135 | — |
| th03-main / Combo HUD and chain | af1131a | Verified | 2 | 978 | — |
| th03-main / Player shots | af1132b | Verified | 1 | 449 | — |
| th03-main / Player effects | af1133a | Verified | 1 | 628 | — |
| th03-main / CPU controller | af1103d | Verified | 1 | 1,077 | — |
| th03-mainl / Staff Roll | af942s | Verified | 1 | 3,695 | 224 |
| th03-mainl / Root controller | af944r | Verified | 1 | 2,458 | 112 |

th03-main Shared BOSS: `.analysis/work/exatt-layout-af1109c/report.json`.

th03-main Ellen Extra Attack: `.analysis/work/exatt-layout-af1129e/report.json`.

th03-main Yumemi Extra Attack: `.analysis/work/exatt-layout-af1127g/report.json`.

th03-main Mima Extra Attack: `.analysis/work/exatt-layout-af1128c/report.json`.

th03-main Reimu Extra Attack: `.analysis/work/exatt-layout-af1112h/report.json`.

th03-main Marisa Extra Attack: `.analysis/work/exatt-layout-af1113c/report.json`.

th03-main Kotohime Extra Attack: `.analysis/work/exatt-layout-af1121d/report.json`.

th03-main Chiyuri Extra Attack: `.analysis/work/exatt-layout-af1122c/report.json`.

th03-main Rikako Extra Attack: `.analysis/work/exatt-layout-af1124d/report.json`.

th03-main Kana Extra Attack: `.analysis/work/exatt-layout-af1125e/report.json`.

th03-main Rikako BOSS: `.analysis/work/exatt-layout-af1118e/report.json`.

th03-main Kana BOSS: `.analysis/work/exatt-layout-af1117f/report.json`.

th03-main Chiyuri BOSS: `.analysis/work/exatt-layout-af1119b/report.json`.

th03-main Kotohime BOSS: `.analysis/work/exatt-layout-af1123e/report.json`.

th03-main Reimu BOSS: `.analysis/work/exatt-layout-af1104e/report.json`.

th03-main Mima BOSS: `.analysis/work/exatt-layout-af1105d/report.json`.

th03-main Marisa BOSS: `.analysis/work/exatt-layout-af1110d/report.json`.

th03-main Ellen BOSS: `.analysis/work/exatt-layout-af1111e/report.json`.

th03-main Yumemi BOSS: `.analysis/work/exatt-layout-af1130c/report.json`.

th03-main Bullet engine: `.analysis/work/exatt-layout-af1107c/report.json`.

th03-main Fireball engine: `.analysis/work/exatt-layout-af1108e/report.json`.

th03-main Enemy engine: `.analysis/work/exatt-layout-af1114e/report.json`.

th03-main Explosion collision: `.analysis/work/exatt-layout-af1120c/report.json`.

th03-main Hitbox and HitCircle: `.analysis/work/exatt-layout-af1101g/report.json`.

th03-main Background chains: `.analysis/work/exatt-layout-af1115b/report.json`.

th03-main MAIN entry and round: `.analysis/work/exatt-layout-af1126c/report.json`.

th03-main Player core: `.analysis/work/exatt-layout-af1116g/report.json`.

th03-main Combo HUD and chain: `.analysis/work/exatt-layout-af1131a/report.json`.

th03-main Player shots: `.analysis/work/exatt-layout-af1132b/report.json`.

th03-main Player effects: `.analysis/work/exatt-layout-af1133a/report.json`.

th03-main CPU controller: `.analysis/work/exatt-layout-af1103d/report.json`.

th03-mainl Staff Roll / 19 procedures: `.analysis/work/mainl-staff-af942s-native-build.json`.

th03-mainl Root controller / 11 procedures: `.analysis/work/mainl-root-af944r-native-build.json`.

## Decoded publication status

OP current decoded source acceptance: 60 extents / 92 procedures / 14,985 bytes (13,221 CODE + 1,764 initialized DATA). Validated source-only cold pair and complete native ownership/ABI pass; older runtime observations remain historical support. Canonical packed-file unit credit and whole-product source exactness remain unchanged; whole-game percentage is unknown.

MAINL decoded source acceptance: 220 extents / 290 procedures or entries / 37,968 bytes (34,431 CODE, 3,531 initialized DATA and 6 reserved file DATA). Origins: 17,717 authored and 20,251 library bytes. Whole-product acceptance is open.

Current native refresh `af1055m` recompiles the complete Staff/root owners in two original TC4 rounds, with target-equal complete decoded EXE/MAP and ordered relocations. The unchanged 938-output cold pair and other selected native providers are revalidated and reused. No full cold rebuild or ancestor runtime replay was performed.

ZUN decoded source acceptance: 77 extents / 89 procedures or entries / 6,179 CODE + 2,456 DATA bytes. Origins: 2,179 authored, 1,390 original ASM and 5,066 library bytes. Twelve reserved DATA bytes and physical devices remain open.

Factory whole-product acceptance remains open for every product. See the [current handoff](RE_HANDOFF.md) and [workflow](RE_WORKFLOW.md).
