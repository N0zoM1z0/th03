# TH03 reconstruction handoff

Reconstruction resumed on 2026-10-07 after the historical 2026-10-06 closeout.
This remains an incomplete, verified repository state: the reviewed MAIN authored
frontier advanced, but a complete maintained game build and the 505-file intake
are unfinished. See CLOSEOUT.md for the earlier frozen snapshot.

## Preserved state

| Artifact | Preserved reviewed result | Acceptance |
| --- | --- | --- |
| MAIN | 62 reviewed authored units / 268 functions / 42268 bytes; exact subset 56 units / 211 functions / 30528 bytes | Boundary-reviewed frontier with scoped repository-local exact subset |
| OP | 40 reviewed decoded units / 12386 bytes; 33 source-present extents / 12019 bytes | exact0 |
| MAINL | 145 decoded rows; 34 source-present extents / 3073 bytes | exact0 |
| ZUN | 18 rows; three source-present wrapper TUs / 234 bytes | exact0 |

MAIN's 30528 exact bytes comprise 30080 function bytes and 448 explicitly
classified producer/table/alignment bytes. The latest accepted default aggregate
is
.analysis/th03-main-exact/gpt-web-yumemi-boss-promote-final-p03x-20261007/receipt.json.
It passes two fresh compilations/links and the maintained DOS behavior probes
with 20 product outputs, 371 deterministic game objects and 437 validated
generated OMF objects. Nine Research-only benchmark objects retain normalized
diagnostic drift outside the declared game vector and do not affect this
acceptance. The earlier Rikako charge/gauge promotion remains preserved at
.analysis/th03-main-exact/gpt-web-rikako-charge-promoted-default-b01-20261007/receipt.json. After local artifact cleanup and source-comment/document
normalization, the current source tree was replayed again successfully at
.analysis/th03-main-exact/gpt-web-housekeeping-final-h02-20261007/receipt.json;
the then-current exact counts and binary outputs were unchanged. After expanding
the reviewed frontier into MAIN_03_TEXT, the earlier 175-function subset was
replayed successfully at
.analysis/th03-main-exact/gpt-web-main-boss-boundary-r01-20261007/receipt.json;
the shared boss prefix and Marisa are now promoted beyond that checkpoint.
The complete enemy owner remains exact: three extents / 19 functions / 3325 bytes.
A consecutive two-producer reconstruction split reproduces the previously failing
ordered ENEMY_2_TEXT relocation list without changing CODE bytes or weakening the
comparison. Historical source filenames remain unknown; see
reconstruction/MAIN_ENEMY_REVIEW.md.

The complete MAIN_05_TEXT character-bomb CODE owner is now exact: one 3113-byte
extent / seven functions produced by five consecutive natural TC4 C++ objects.
Chiyuri contributes 490 bytes, Ellen 1023 across three functions, Kana 526,
Kotohime 528, and Rikako 546. Their MAP contributions cover
183C:0001..0C29 exactly, all 3113 linked bytes match the immutable target, and
the complete 71-entry MZ relocation order matches in both fresh default replay
rounds.

This promotion preserves the failed symbolic-TASM attempt as a negative control.
Five TASM pieces reproduce the bytes and relocation sites but not relocation
order; the exact result requires the observed TC4J producer/FIXUPP behavior.
The C++ producers refer to semantic private-state names, while the frozen
carrier exports those names at the already-symbolized TH03 BSS locations:
Ellen 25DC/25DE/265E, Kana 2674, Kotohime 28F6, and Rikako 4B8C. That binding
restores the original references without hard-coded target addresses in C++.
Only the CODE extent is promoted here: historical physical BSS producer
ownership remains a separate open question. See
reconstruction/MAIN_BOMBS_REVIEW.md.

The next authored frontier is target-reviewed rather than guessed.
MAIN_07_TEXT through MAIN_11_TEXT form five complete character-local
charge-shot/gauge owners: Chiyuri 1011 bytes / 9 functions, Ellen 1530 / 10,
Kana 1291 / 9, Kotohime 690 / 9, and Rikako 1280 / 11. Together they cover
5802 reviewed bytes / 48 functions with all 60 in-owner relocations recorded.
Chiyuri MAIN_07_TEXT is exact: one natural TC4J producer reproduces all
1011 linked bytes, the exact MAP contribution and the ordered relocation
sequence 956,892,879,794,775,434,331,299,199. Its C++ object emits no private
BSS; the frozen carrier exposes semantic names at the unchanged historical
1F54/1F58/1F5A/1F51A/2D58 state slots.

Ellen MAIN_08_TEXT is exact as well: one natural TC4J producer reproduces all
1530 linked bytes, the exact MAIN_08_TEXT MAP contribution, and all 22 ordered
relocations. Kana MAIN_09_TEXT and Kotohime MAIN_10_TEXT complete the same gate:
their natural producers reproduce all 1291 and 690 linked bytes respectively,
their exact MAP contributions, and all ordered relocations. None of these C++
objects emits private DATA/BSS; frozen-carrier aliases preserve the historical
state slots.

Rikako MAIN_11_TEXT is now exact too. One natural TC4J cs_rika producer
reproduces all 1280 linked bytes / 11 functions, the exact 1C40:000A..0509
MAP contribution and all 12 ordered relocations. Its 476-instruction object
shape matches the immutable target and emits zero private DATA/BSS. Carrier
aliases bind gauge-frame/charge state at unchanged DGROUP offsets
38F4/38F6/3926/3928/392A/392C/3930/3934. The five reviewed
charge-shot/gauge owners are therefore all exact. That family ended at
175 exact functions / 23868 owned bytes; the later boss-prefix promotion raises
the current aggregate further. See reconstruction/MAIN_CHARGE_GAUGE_REVIEW.md.

The reviewed frontier now includes the complete MAIN_03_TEXT boss-attack
segment. Target-first review partitions all 18400 bytes into one shared helper
owner plus nine character-local owners, with 93 complete functions / 17683
function bytes and nine explicitly classified Turbo C++ switch tables / 717
producer-owned bytes. All 326 in-owner MZ relocations are recorded and no
relocation crosses an owner edge.

The first three logical boss owners are now exact. The 949-byte shared prefix /
eight functions is maintained as one semantic natural source but uses two
consecutive TC4J physical producers (348-byte explosion ring + 601-byte
remainder) because the one-object model reversed the two historical FIXUPP
relocation groups. A zero-byte TASM order scaffold preserves TLINK first-seen
segment order and owns no game bytes. Marisa contributes 1431 bytes / nine
functions plus an 81-byte switch table. Mima now contributes 1922 bytes / nine
functions plus its 81-byte switch table, including the 298-byte update and
305-byte render helper. Mima matches all linked bytes and all 32 ordered
relocations in two default cold builds, emits no private DATA/BSS, and aliases
render/parameter/orbit state at the observed carrier storage. The first four logical boss owners are now exact. Yumemi contributes 2358
bytes / ten functions plus its 80-byte compiler switch table, including the
368-byte update, 333-byte main renderer and 404-byte arrival renderer. Its one
natural TC4J producer matches all linked bytes, exact MAP placement and all 61
ordered relocations in two default cold builds and emits zero private DATA/BSS.
Carrier aliases preserve the observed boss, parameter, fixed table and private
scratch storage. Reimu is the next complete owner. See
reconstruction/MAIN_BOSS_REVIEW.md.

Japanese YUMEZIKU targets remain pinned in `config/targets.toml`, with
candidate-local-attested provenance; independent pristine-dump confirmation
is unknown. Frozen ReC98 revision:
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`. Reference or cross-game exactness
is never inherited. Stored OP/MAINL/ZUN and restored diagnostic namespaces
remain distinct; decoded rows do not invent packed-file offsets.

The intake has 505 files. MAIN has 70 paths with scoped CODE review; MAINL has
33 direct-source CODE-only index rows, with source/exact acceptance false.
Those different scopes must not be added into a completed-file count.
[Review index](REC98_TH03_REVIEW.md), CSV ledgers and [progress](PROGRESS.md)
retain the detailed ownership and evidence.

## Latest maintained decoded source

Shared CDG load/free593, drawing496, text613, LUT30, sound loader112 and PI
palette/put/load243 have independent OP/MAINL bindings. MAINL additionally
owns the natural vector ASM160 and PI interlace/quarter312. Input/timing has
four complete natural CPP carriers535: shared388, OP21, MAINL126. Twelve
existing MAINL rows were upgraded without duplicate interval credit.

The latest two-round decoded source receipt is
`.analysis/th03-shared-input/sol-shared-input-source-20261006-b/receipt.json`,
SHA256 `37d956f61667d1ba35589989286aaa54d55b9cc8ee121743c0d70dd63d32cbeb`.
It guards733inputs, records20products/351gameobjects/417OMF, preserves original
carrier bytes/ordered relocations/nondependency records/MAP/publics, and
keeps Research nongame changes separate. Native OP278/MAINL321 positions are
covered under explicit BIOS/joystick/driver/clock models. Scanner417/trailing
NOP remains contextual to this migration. See
[input/timing review](reconstruction/SHARED_INPUT_REVIEW.md).

Current interval coverage:
`.analysis/sol-current-decoded-coverage-after-shared-input-20261006.json`,
SHA256 `efdd19c333d0d41ccb8a46d3297de7816cade5cd632a2ff64d26e6deb6209f8b`.
OP:12386/55262 reviewed bytes,42876gaps; MAINL:28381/58340,29959gaps.
Both current cold MAPs have zero overlap. Historical shifted MAP comparisons
remain historical; their earlier failures are not replaced by this result.

## Unfinished acceptance

Whole OP retains six changed decoded bytes and313 unequal original relocation
rows, despite the same607-site multiset. Whole MAINL retains21 changed bytes
and original relocation-order failure. Historical MAIN-overlay comparisons
retain their independent4867-byte OP and340-byte MAINL failures.

MAIN's remaining root code/data and physical main.obj ownership, MAINL CRT,
headers/global DATA/BSS, native devices/IRQ/timing, heap/file/graphics/assets,
canonical DIET storage and complete product/Oracle/Factory acceptance remain
open. Native runtime fixtures are declared models. Prefixes are bounded
execution observations, not successful termination. No new exactness follows
from cleanup or a reference/compiler smoke build.

## Maintenance and evidence

Product source and Oracle-bearing scripts stay at their attested paths. Detailed
history lives in reconstruction/README.md, the CSV ledgers and Git. Targets,
runtime images, the game-local Wine prefix, Ghidra projects, referenced proof
inputs, cold receipt trees and meaningful failed transcripts are retained.

For verification, run:

    python3 scripts/preflight.py
    python3 scripts/replay_th03_main_exact_units.py --run-id UNIQUE_ID
    python3 scripts/ci.py
    git diff --check

Use headless tools and one Borland/Wine writer. Re-attest a selected Ghidra
database before new target observations. Continue MAIN with the complete Reimu boss owner, then the remaining reviewed
boss owners, while expanding root code/data ownership and the maintained build
graph; do not treat the reviewed authored frontier as
whole-product completion.

Historical closeout CI was 607 tests / 50.517 seconds with available private
headless gates passing at the 2026-10-06 snapshot. Current preflight tracking is
265 units / 2451 evidence rows / three hypotheses / 316 knowledge rows / 268
MAIN authored-function rows. The scoped exact subset is now 211 functions /
30528 owned bytes. The remaining six MAIN_03_TEXT character owners stay
boundary-reviewed; Reimu is the next complete source/full-link target.

The current Factory host no longer has the historical Conda Python/Unicorn
installation. The latest /usr/bin/python3 CI attempt runs 621 tests but reports
125 errors, all 125 ending in ModuleNotFoundError for the missing unicorn module,
with 167 skips; its log is
.analysis/th03-main-exact/gpt-web-yumemi-boss-promote-final-p03x-20261007/ci-current-host.log.
No local wheel, egg, apt cache, or alternate Python with Unicorn is present.
The CI steps after unittest were rerun individually and pass: compileall,
tracking, progress, MAINL intake policy, TH03 inventory, target verification,
Oracle smoke, toolchain and analysis-toolchain attestations, all available TH03
Ghidra database checks and negative controls, and git diff --check. Their log is
.analysis/th03-main-exact/gpt-web-yumemi-boss-promote-final-p03x-20261007/ci-post-unittest-gates.log.
This is an explicit host dependency block, not a full-CI PASS.
