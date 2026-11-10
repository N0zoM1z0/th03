# TH03 reconstruction progress

All counts describe repository-local tracked scopes. The whole-game completion percentage is unknown.

| Product | Source-present / tracked extents | Current accepted scope | Stored target bytes |
| --- | ---: | --- | ---: |
| th03-op | 62/62 | Decoded: 60 extents / 14,985 bytes | 36,041 |
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
| th03-main / VRAM plane initializer | af1326e | Verified | 1 | 41 | — |
| th03-main / Stage demo transition | af1333a | Verified | 1 | 663 | — |
| th03-main / Shared BOSS | af1326i | Verified | 2 | 949 | — |
| th03-main / PI image loader | af1322i | Verified | 1 | 70 | — |
| th03-main / DOS executable handoff | af1322j | Verified | 1 | 79 | — |
| th03-main / Resident CFG loader | af1182a | Verified | 1 | 49 | — |
| th03-main / PC-98 shutdown | af1184d | Verified | 1 | 67 | — |
| th03-main / Input modes and keyboard wait | af1313c | Verified | 1 | 367 | — |
| th03-main / PMD/MIDI audio services | af1320b | Verified | 2 | 150 | — |
| th03-main / Signed Q8 polar geometry | af1322h | Verified | 1 | 26 | — |
| th03-main / Volatile VSYNC frame delay | af1316e | Verified | 1 | 21 | — |
| th03-main / DOS MAIN initializer | af1316f | Verified | 1 | 62 | — |
| th03-main / Ellen Extra Attack | af1129e | Verified | 1 | 1,129 | — |
| th03-main / Yumemi Extra Attack | af1200c | Verified | 1 | 1,696 | — |
| th03-main / Mima Extra Attack | af1306e | Verified | 1 | 727 | — |
| th03-main / Reimu Extra Attack | af1112h | Verified | 2 | 1,156 | — |
| th03-main / Marisa Extra Attack | af1196d | Verified | 1 | 676 | — |
| th03-main / Kotohime Extra Attack | af1199e | Verified | 1 | 1,054 | — |
| th03-main / Chiyuri Extra Attack | af1122c | Verified | 1 | 978 | — |
| th03-main / Rikako Extra Attack | af1301f | Verified | 1 | 702 | — |
| th03-main / Kana Extra Attack | af1302f | Verified | 1 | 663 | — |
| th03-main / Rikako BOSS | af1321h | Verified | 1 | 1,677 | — |
| th03-main / Kana BOSS | af1323f | Verified | 1 | 1,874 | — |
| th03-main / Chiyuri BOSS | af1329l | Verified | 1 | 2,654 | — |
| th03-main / Kotohime BOSS | af1319e | Verified | 1 | 1,840 | — |
| th03-main / Reimu BOSS | af1336i | Verified | 1 | 2,020 | — |
| th03-main / Mima BOSS | af1317k | Verified | 1 | 1,922 | — |
| th03-main / Marisa BOSS | af1325h | Verified | 1 | 1,431 | — |
| th03-main / Ellen BOSS | af1331h | Verified | 1 | 1,675 | — |
| th03-main / Yumemi BOSS | af1334f | Verified | 1 | 2,358 | — |
| th03-main / Bullet engine | af1318f | Verified | 1 | 2,685 | — |
| th03-main / Fireball engine | af1325i | Verified | 1 | 1,555 | — |
| th03-main / Enemy engine | af1310h | Verified | 4 | 3,325 | — |
| th03-main / Explosion collision | af1198g | Verified | 1 | 630 | — |
| th03-main / Hitbox and HitCircle | af1317l | Verified | 2 | 711 | — |
| th03-main / Background chains | af1115b | Verified | 2 | 1,245 | — |
| th03-main / MAIN entry and round | af1314c | Verified | 1 | 3,050 | — |
| th03-main / Round results and reset | af1164e | Verified | 1 | 1,060 | — |
| th03-main / Round intro HUD | af1166i | Verified | 1 | 1,478 | — |
| th03-main / Static HUD | af1165h | Verified | 1 | 539 | — |
| th03-main / Player core | af1191e | Verified | 1 | 3,135 | — |
| th03-main / Player loss and defeat | af1163i | Verified | 1 | 664 | — |
| th03-main / Gauge and shared Extra Attack | af1324e | Verified | 2 | 96 | — |
| th03-main / Marisa Chargeshot | af1134f | Verified | 1 | 1,509 | — |
| th03-main / Chiyuri Chargeshot | af1135h | Verified | 1 | 1,011 | — |
| th03-main / Reimu Chargeshot | af1136f | Verified | 1 | 1,448 | — |
| th03-main / Ellen Chargeshot | af1138f | Verified | 1 | 1,530 | — |
| th03-main / Rikako Chargeshot | af1140e | Verified | 1 | 1,280 | — |
| th03-main / Kana Chargeshot | af1141f | Verified | 1 | 1,291 | — |
| th03-main / Mima Chargeshot | af1142d | Verified | 1 | 1,338 | — |
| th03-main / Yumemi Chargeshot | af1143h | Verified | 1 | 1,645 | — |
| th03-main / Kotohime Chargeshot | af1146d | Verified | 1 | 690 | — |
| th03-main / Ellen Bomb | af1147c | Verified | 1 | 1,023 | — |
| th03-main / Rikako Bomb | af1148f | Verified | 1 | 546 | — |
| th03-main / Mima Bomb | af1149e | Verified | 1 | 833 | — |
| th03-main / Yumemi Bomb | af1152f | Verified | 1 | 698 | — |
| th03-main / Reimu Bomb and shared lifecycle | af1153d | Verified | 1 | 925 | — |
| th03-main / Kotohime Bomb | af1154d | Verified | 1 | 528 | — |
| th03-main / Kana Bomb | af1155b | Verified | 1 | 526 | — |
| th03-main / Chiyuri Bomb | af1156b | Verified | 1 | 490 | — |
| th03-main / Marisa Bomb | af1159d | Verified | 1 | 449 | — |
| th03-main / Combo HUD and chain | af1131a | Verified | 2 | 978 | — |
| th03-main / Player shots | af1132b | Verified | 1 | 449 | — |
| th03-main / Player effects | af1133a | Verified | 1 | 628 | — |
| th03-main / Warning and Gauge HUD | af1160e | Verified | 1 | 1,560 | — |
| th03-main / Character callback setup | af1161f | Verified | 1 | 3,888 | — |
| th03-main / CPU controller | af1327h | Verified | 1 | 1,077 | — |
| th03-main / Shared sound assembler leaves | af1328b | Verified | 3 | 100 | — |
| th03-main / Graphics and asset assembler leaves | af1330f | Verified | 6 | 1,622 | — |
| th03-main / Vector, playfield and collision ASM | af1332c | Verified | 3 | 710 | — |
| th03-main / Round RNG and collision reset ASM | af1333c | Verified | 1 | 82 | — |
| th03-main / VSYNC initialized storage ASM | af1337i | Verified | 1 | 0 | — |
| th03-main / Original master library CODE carriers | af1338c | Verified | 2 | 10,570 | — |
| th03-mainl / Staff Roll | af942s | Verified | 1 | 3,695 | 224 |
| th03-mainl / Root controller | af944r | Verified | 1 | 2,458 | 112 |

th03-main VRAM plane initializer: `.analysis/work/exatt-layout-af1326e/report.json`.

th03-main Stage demo transition: `.analysis/work/exatt-layout-af1333a/report.json`.

th03-main Shared BOSS: `.analysis/work/exatt-layout-af1326i/report.json`.

th03-main PI image loader: `.analysis/work/exatt-layout-af1322i/report.json`.

th03-main DOS executable handoff: `.analysis/work/exatt-layout-af1322j/report.json`.

th03-main Resident CFG loader: `.analysis/work/exatt-layout-af1182a/report.json`.

th03-main PC-98 shutdown: `.analysis/work/exatt-layout-af1184d/report.json`.

th03-main Input modes and keyboard wait: `.analysis/work/exatt-layout-af1313c/report.json`.

th03-main PMD/MIDI audio services: `.analysis/work/exatt-layout-af1320b/report.json`.

th03-main Signed Q8 polar geometry: `.analysis/work/exatt-layout-af1322h/report.json`.

th03-main Volatile VSYNC frame delay: `.analysis/work/exatt-layout-af1316e/report.json`.

th03-main DOS MAIN initializer: `.analysis/work/exatt-layout-af1316f/report.json`.

th03-main Ellen Extra Attack: `.analysis/work/exatt-layout-af1129e/report.json`.

th03-main Yumemi Extra Attack: `.analysis/work/exatt-layout-af1200c/report.json`.

th03-main Mima Extra Attack: `.analysis/work/exatt-layout-af1306e/report.json`.

th03-main Reimu Extra Attack: `.analysis/work/exatt-layout-af1112h/report.json`.

th03-main Marisa Extra Attack: `.analysis/work/exatt-layout-af1196d/report.json`.

th03-main Kotohime Extra Attack: `.analysis/work/exatt-layout-af1199e/report.json`.

th03-main Chiyuri Extra Attack: `.analysis/work/exatt-layout-af1122c/report.json`.

th03-main Rikako Extra Attack: `.analysis/work/exatt-layout-af1301f/report.json`.

th03-main Kana Extra Attack: `.analysis/work/exatt-layout-af1302f/report.json`.

th03-main Rikako BOSS: `.analysis/work/exatt-layout-af1321h/report.json`.

th03-main Kana BOSS: `.analysis/work/exatt-layout-af1323f/report.json`.

th03-main Chiyuri BOSS: `.analysis/work/exatt-layout-af1329l/report.json`.

th03-main Kotohime BOSS: `.analysis/work/exatt-layout-af1319e/report.json`.

th03-main Reimu BOSS: `.analysis/work/exatt-layout-af1336i/report.json`.

th03-main Mima BOSS: `.analysis/work/exatt-layout-af1317k/report.json`.

th03-main Marisa BOSS: `.analysis/work/exatt-layout-af1325h/report.json`.

th03-main Ellen BOSS: `.analysis/work/exatt-layout-af1331h/report.json`.

th03-main Yumemi BOSS: `.analysis/work/exatt-layout-af1334f/report.json`.

th03-main Bullet engine: `.analysis/work/exatt-layout-af1318f/report.json`.

th03-main Fireball engine: `.analysis/work/exatt-layout-af1325i/report.json`.

th03-main Enemy engine: `.analysis/work/exatt-layout-af1310h/report.json`.

th03-main Explosion collision: `.analysis/work/exatt-layout-af1198g/report.json`.

th03-main Hitbox and HitCircle: `.analysis/work/exatt-layout-af1317l/report.json`.

th03-main Background chains: `.analysis/work/exatt-layout-af1115b/report.json`.

th03-main MAIN entry and round: `.analysis/work/exatt-layout-af1314c/report.json`.

th03-main Round results and reset: `.analysis/work/exatt-layout-af1164e/report.json`.

th03-main Round intro HUD: `.analysis/work/exatt-layout-af1166i/report.json`.

th03-main Static HUD: `.analysis/work/exatt-layout-af1165h/report.json`.

th03-main Player core: `.analysis/work/exatt-layout-af1191e/report.json`.

th03-main Player loss and defeat: `.analysis/work/exatt-layout-af1163i/report.json`.

th03-main Gauge and shared Extra Attack: `.analysis/work/exatt-layout-af1324e/report.json`.

th03-main Marisa Chargeshot: `.analysis/work/exatt-layout-af1134f/report.json`.

th03-main Chiyuri Chargeshot: `.analysis/work/exatt-layout-af1135h/report.json`.

th03-main Reimu Chargeshot: `.analysis/work/exatt-layout-af1136f/report.json`.

th03-main Ellen Chargeshot: `.analysis/work/exatt-layout-af1138f/report.json`.

th03-main Rikako Chargeshot: `.analysis/work/exatt-layout-af1140e/report.json`.

th03-main Kana Chargeshot: `.analysis/work/exatt-layout-af1141f/report.json`.

th03-main Mima Chargeshot: `.analysis/work/exatt-layout-af1142d/report.json`.

th03-main Yumemi Chargeshot: `.analysis/work/exatt-layout-af1143h/report.json`.

th03-main Kotohime Chargeshot: `.analysis/work/exatt-layout-af1146d/report.json`.

th03-main Ellen Bomb: `.analysis/work/exatt-layout-af1147c/report.json`.

th03-main Rikako Bomb: `.analysis/work/exatt-layout-af1148f/report.json`.

th03-main Mima Bomb: `.analysis/work/exatt-layout-af1149e/report.json`.

th03-main Yumemi Bomb: `.analysis/work/exatt-layout-af1152f/report.json`.

th03-main Reimu Bomb and shared lifecycle: `.analysis/work/exatt-layout-af1153d/report.json`.

th03-main Kotohime Bomb: `.analysis/work/exatt-layout-af1154d/report.json`.

th03-main Kana Bomb: `.analysis/work/exatt-layout-af1155b/report.json`.

th03-main Chiyuri Bomb: `.analysis/work/exatt-layout-af1156b/report.json`.

th03-main Marisa Bomb: `.analysis/work/exatt-layout-af1159d/report.json`.

th03-main Combo HUD and chain: `.analysis/work/exatt-layout-af1131a/report.json`.

th03-main Player shots: `.analysis/work/exatt-layout-af1132b/report.json`.

th03-main Player effects: `.analysis/work/exatt-layout-af1133a/report.json`.

th03-main Warning and Gauge HUD: `.analysis/work/exatt-layout-af1160e/report.json`.

th03-main Character callback setup: `.analysis/work/exatt-layout-af1161f/report.json`.

th03-main CPU controller: `.analysis/work/exatt-layout-af1327h/report.json`.

th03-main Shared sound assembler leaves: `.analysis/work/main-sound-asm-af1328b/report.json`.

th03-main Graphics and asset assembler leaves: `.analysis/work/main-graphics-asm-af1330f/report.json`.

th03-main Vector, playfield and collision ASM: `.analysis/work/main-geometry-asm-af1332c/report.json`.

th03-main Round RNG and collision reset ASM: `.analysis/work/main-roundpr-asm-af1333c/report.json`.

th03-main VSYNC initialized storage ASM: `.analysis/work/main-vsync-storage-asm-af1337i/report.json`.

th03-main Original master library CODE carriers: `.analysis/work/main-master-library-asm-af1338c/report.json`.

th03-mainl Staff Roll / 19 procedures: `.analysis/work/mainl-staff-af942s-native-build.json`.

th03-mainl Root controller / 11 procedures: `.analysis/work/mainl-root-af944r-native-build.json`.

## Decoded publication status

OP current decoded source acceptance: 60 extents / 92 procedures / 14,985 bytes (13,221 CODE + 1,764 initialized DATA). Validated source-only cold pair and complete native ownership/ABI pass; older runtime observations remain historical support. Canonical packed-file unit credit and whole-product source exactness remain unchanged; whole-game percentage is unknown.

MAINL decoded source acceptance: 220 extents / 290 procedures or entries / 37,968 bytes (34,431 CODE, 3,531 initialized DATA and 6 reserved file DATA). Origins: 17,717 authored and 20,251 library bytes. Whole-product acceptance is open.

Current native refresh `af1055m` recompiles the complete Staff/root owners in two original TC4 rounds, with target-equal complete decoded EXE/MAP and ordered relocations. The unchanged 938-output cold pair and other selected native providers are revalidated and reused. No full cold rebuild or ancestor runtime replay was performed.

ZUN decoded source acceptance: 77 extents / 89 procedures or entries / 6,179 CODE + 2,456 DATA bytes. Origins: 2,179 authored, 1,390 original ASM and 5,066 library bytes. Twelve reserved DATA bytes and physical devices remain open.

Factory whole-product acceptance remains open for every product. See the [current handoff](RE_HANDOFF.md) and [workflow](RE_WORKFLOW.md).
