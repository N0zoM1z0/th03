# TH03 reconstruction handoff

Reconstruction resumed on 2026-10-07 after the historical 2026-10-06 closeout.
This remains an incomplete, verified repository state: the reviewed MAIN authored
frontier advanced, but a complete maintained game build and the 505-file intake
are unfinished. See CLOSEOUT.md for the earlier frozen snapshot.

## Preserved state

| Artifact | Preserved reviewed result | Acceptance |
| --- | --- | --- |
| MAIN | 73 reviewed authored units / 330 functions / 51644 bytes; exact subset 73 units / 330 functions / 51644 bytes | Boundary-reviewed frontier with scoped repository-local exact subset |
| OP | 40 reviewed decoded units / 12386 bytes; 33 source-present extents / 12019 bytes | exact0 |
| MAINL | 145 decoded rows; 34 source-present extents / 3073 bytes | exact0 |
| ZUN | 18 rows; three source-present wrapper TUs / 234 bytes | exact0 |

MAIN's 51644 exact bytes comprise 50721 function bytes and 923 explicitly
classified producer/table/alignment bytes. The latest accepted default aggregate
is
.analysis/th03-main-exact/gpt-web-hyper-main010-default-p01-20261008/receipt.json.
It passes two fresh compilations/links and the maintained DOS behavior probes
with 20 product outputs, 390 deterministic game objects and 456 validated
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

At that checkpoint, the next authored frontier was target-reviewed rather than guessed.
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

All ten logical boss owners are now exact. The 949-byte shared prefix /
eight functions is maintained as one semantic natural source but uses two
consecutive TC4J physical producers to preserve historical FIXUPP ordering; a
zero-byte TASM scaffold preserves TLINK first-seen segment order and owns no
game bytes. Marisa contributes 1431 bytes / nine functions plus an 81-byte
switch table; Mima contributes 1922 / nine plus 81; Yumemi contributes 2358 /
ten plus 80; Reimu contributes 2020 / nine plus 72; Ellen contributes 1675 /
nine plus 81; and Kotohime contributes 1840 / eleven plus 80. Kotohime includes
the 302-byte radial-burst pattern, 332-byte update and 188-byte ring renderer.
Its natural ba_koto producer matches all 1840 linked bytes, exact MAP placement
and all 24 ordered relocations in two default cold builds and emits zero private
DATA/BSS. Carrier aliases preserve the seven shared level-derived parameters
and the existing boss-state radius/angle/frame storage without moving data.
Chiyuri now contributes 2654 exact bytes / eleven functions plus its 81-byte
switch table. Its natural ba_chiyu producer matches every linked byte, exact
MAP placement and all 49 ordered relocations in two default cold builds. The
352-byte cardinal pattern, 528-byte fan pattern and 613-byte update are all
maintained as natural source; the object emits zero private DATA/BSS. Carrier
aliases preserve the seven shared parameters, two private direction bytes and
five-position coordinate table without moving storage. Kana now contributes
1874 exact bytes / nine functions plus its 80-byte compiler switch table. Its
natural ba_kana producer matches every linked byte, exact MAP placement and all
35 ordered relocations in two default cold builds, including the 321-byte
staged-ring pattern, 316-byte update and 219-byte intro renderer. The object
emits zero private DATA/BSS and carrier aliases preserve the seven shared
parameters plus the private rotating angle/delta without moving storage.
Rikako completes the segment with 1677 exact bytes / eight functions plus an
81-byte padded switch table. Its natural ba_rikak producer matches every linked
byte, exact MAP placement and all 30 ordered relocations; carrier aliases keep
the five shared parameters, signed spin-delta field and private random/type
bytes at their observed historical locations. Therefore the complete
18400-byte MAIN_03_TEXT boss-attack segment is exact within the repository
Oracle scope. See reconstruction/MAIN_BOSS_REVIEW.md.

The reviewed frontier now expands into the complete remaining character Extra
Attack family around the already exact 41-byte generic P_EXATT_TEXT owner.
Target-first review partitions 8781 additional bytes into ten complete owners:
five P_EXATT_TEXT character owners and a MAIN_06_TEXT shared/Reimu/Mima/Yumemi/
Rikako family. They contain 52 complete functions and all 140 in-owner MZ
relocations; no relocation crosses an owner edge. The largest function is
Yumemi's 1150-byte helper, alongside 470-byte Ellen and 398-byte Mima updates.
All ten reviewed Extra Attack character/shared owners are now CODE exact. Chiyuri (1029
bytes / five functions, including its 518-byte beam renderer, 298-byte
paired updater and the 51-byte Ellen-slot initializer) is now exact as a
real TC4J producer before the frozen carrier. A zero-byte TASM ordering
object retains the original PELLET/BULLET/E_FIREB/MAIN_05/P_EXATT segment
order; MAP and all 23 Chiyuri ordered MZ relocations match without moving
private DATA/BSS. The natural-source Kana (663 bytes / five including
244-byte update), Marisa (676 bytes / five
including a 251-byte update) and Kotohime (1054 bytes / eight including the
351-byte update) P_EXATT_TEXT suffix are
exact, as is the immediately following 41-byte generic owner and contiguous
4281-byte MAIN_06_TEXT family: shared flight (215 / two functions),
Reimu (941 / eight including shared renderer/collision helpers), Mima
(727 / four), Yumemi (1696 / five including the 1150-byte renderer), and
Rikako (702 / five). Six physical natural TC4J objects reconstruct that
segment, including two consecutive producers for Reimu to preserve original
FIXUPP order. Raw bytes, MAP and all 4 + 14 + 10 + 36 + 9 ordered MZ
relocations match in two default cold links. The earlier single-producer
Reimu failure and initial shared-helper shape experiments are preserved as
negative controls. Together with Ellen (1078 / five functions including the 470-byte update)
and Chiyuri (1029 / five including the 518-byte renderer), the ten complete
Extra Attack owners plus the 41-byte generic owner now cover **8822 contiguous
exact CODE bytes** at 18FE:000A..2280; the Kotohime charge-gauge caller now binds
the natural far Pascal helper instead of the obsolete frozen-ASM alias.
No raw game instruction carrier or relaxed comparator was used. Ellen
requires an explicit compiler OMF record-boundary calibration at owner offset
1000: unmodified TC4 CODE and all fixup target/frame descriptors are retained,
while the three following record-relative fixup offsets are rebased by +24.
This establishes scoped exact linked CODE through the maintained local Oracle;
it does not independently recover historical native OMF producer identity.
Historical physical DATA/BSS producer ownership remains open. See
reconstruction/MAIN_EXATT_REVIEW.md.

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
database before new target observations. The complete MAIN_03_TEXT boss segment
remains exact. The active frontier is the Extra Attack family in P_EXATT_TEXT
and MAIN_06_TEXT: the entire shared/Reimu/Mima/Yumemi/Rikako MAIN_06_TEXT
family remains exact. Kotohime (1054 bytes / 8 functions, including the
351-byte update) is additionally exact through a natural TC4J P_EXATT_TEXT
producer with all 15 original ordered relocations. Its charge-gauge caller
was rebound from an old ASM alias to the natural far Pascal helper, without
regressing existing exact bytes. Marisa (676 / five functions including the
251-byte update) is also exact in the immediately preceding P_EXATT_TEXT
segment; its boss-facing far Pascal symbol binds directly to the new TC4J
producer. Kana (663 / five functions, including the 244-byte vector2/
bullet update) is now exact in the immediately preceding segment with all
eight original ordered relocations. Chiyuri (1029 bytes / five functions)
is now exact, with the original 23 ordered relocations and the 51-byte
Ellen BSS-slot initializer moved to maintained source. Ellen (1078 bytes / five functions) is also exact through an explicit
TC4 OMF LEDATA/FIXUPP frame calibration that preserves all 1078 CODE bytes and all fourteen
original MZ relocation sites in their original order. Earlier single TC4,
two-producer and TC4 -S -> TASM experiments failed the strict order gate and
remain documented as negative controls. The final Oracle is unchanged.
Continue reconstructing complete owners rather than isolated leaves, and do not
treat reviewed coverage as whole-product completion.

Historical closeout CI was 607 tests / 50.517 seconds with available private
headless gates passing at the 2026-10-06 snapshot. Current preflight tracking is
276 units / 2603 evidence rows / three hypotheses / 353 knowledge rows / 330
MAIN authored-function rows. The scoped exact subset now covers all 330
reviewed functions / 51644 owned bytes. The whole-game denominator is still
unknown, and OP/MAINL/ZUN are not accepted exact. The ten new Extra Attack owners account for the
52-function / 8781-byte now-exact extension of the reviewed CODE frontier.

The current Factory host does not provide the Python `unicorn` module.
The 2026-10-08 /usr/bin/python3 CI attempt runs 635 tests but reports 125
errors importing this missing module, with 167 skips; the latest full CI
failure is retained at `.analysis/th03-ellen-omf-ci-final-20261008.log` (the earlier
Yumemi/Rikako promotion failure remains at `.analysis/th03-ci-exatt-20261008.log`). The interpreter reports
`importlib.util.find_spec("unicorn") is None`. As before, this is a host
dependency block, not a full-CI PASS or an owner-byte mismatch.

The CI steps after unittest were rerun independently and **pass**: compileall,
tracking, progress, MAINL intake policy, TH03 inventory, target verification,
Oracle smoke, toolchain and analysis-toolchain attestations, all available TH03
Ghidra database checks and negative controls, and git diff --check. Their log
is `.analysis/th03-ellen-omf-postgates-final-20261008.log`; its final line confirms
`POST-UNITTEST GATES: PASS`. The earlier suffix post-gates log is retained too.
The final Kana default exact receipt after ledger updates is
.analysis/th03-main-exact/gpt-web-exatt-kana-default-final-p03-20261008/receipt.json.
The previous Marisa-source default exact receipt after all ledger updates is
.analysis/th03-main-exact/gpt-web-exatt-marisa-default-final-p02-20261008/receipt.json.
The earlier Kotohime-source default exact receipt after ledger updates is
.analysis/th03-main-exact/gpt-web-kotohime-exatt-default-final-p02-20261008/receipt.json.
The preceding shared-flight default exact checkpoint is
`.analysis/th03-main-exact/gpt-web-exatt-shared-default-final-p02-20261008/receipt.json`.
The preceding Reimu exact checkpoint stays preserved at
`.analysis/th03-main-exact/gpt-web-reimu-default-final-p02-20261008/receipt.json`.
The preceding Mima closeout is retained at
`.analysis/th03-main-exact/gpt-web-mima-default-final-p03-20261008/receipt.json`.
The prior Yumemi+Rikako closeout stays preserved at
`.analysis/th03-main-exact/gpt-web-exatt-suffix-default-final-p02-20261008/receipt.json`.
A strict diagnostic replay gpt-web-exatt-kana-default-final-p02-20261008
failed determinism without any changed source inputs, target CODE bytes, MZ
relocations, MAP, game executable product hashes or DOS behavior:
the frozen TASM-generated main.obj has 77 different raw bytes in the two
cold compilations. Dependency timestamp normalization removes six of those
differences, leaving 71, beginning inside a PUBDEF OMF record; the scoped
main.obj and six carrier aliases therefore fail the unchanged normalized
object-hash gate. Receipt preserved in .analysis/th03-main-exact/
gpt-web-exatt-kana-default-final-p02-20261008/receipt.json. The next
independent full default two-round replay
gpt-web-exatt-kana-default-final-p03-20261008 passes all gates with the same
source/manifest hash. This nondeterministic TASM PUBDEF observation is
tracked separately from Research-only timestamp drift and must not be
masked by weakening the existing OMF comparator.

The latest post-ledger/default Chiyuri acceptance receipt is:
.analysis/th03-main-exact/gpt-web-chiyuri-default-final-p02-20261008/receipt.json.
It independently reconfirms 315 function bodies, 49971 owned bytes, the
unaltered original MAP/ordered relocations across all prior owners, 388 game
objects and passing DOS probes. The 518-byte renderer, 298-byte paired
updater and 51-byte Ellen slot initializer are now maintained natural TC4J
CODE owners. A zero-game-byte TASM segment-order object preserves the
historical first-seen MAIN_04, MAIN_05 and P_EXATT_TEXT layout.

No Factory Truth Kernel acceptance is implied by this repository-local result.


Historical **negative Ellen diagnostic** (before the final record framing):
unmodified TC4 and two-object TASM candidates reproduced raw 1078-byte CODE
and MAP, but placed the sound-call relocation site 1003 before the other 13.
Receipt: .analysis/th03-main-exact/gpt-web-ellen-raw-blocker-link-v09-20261008/receipt.json.
The pinned natural TC4 OMF framing correction now makes this owner pass the
**unchanged** ordered-relocation gate in default replay. See
reconstruction/MAIN_EXATT_REVIEW.md for raw compiler and calibrated OMF SHA
evidence; no historical native-toolchain equivalence is claimed.

Historical 310-function default acceptance (before Chiyuri and Ellen)
passed two additional cold links and DOS probes at
.analysis/th03-main-exact/gpt-web-ellen-blocker-default-baseline-b01-20261008/receipt.json.
Full /usr/bin/python3 CI is blocked by the missing host unicorn module:
Historical 632-test CI attempt reported 125 import errors and 167 skips;
retained log: .analysis/th03-ellen-blocker-ci-20261008.log. The five focused Extra Attack
review tests, preflight, tracking, progress and git diff --check pass.

## Reviewed Extra Attack owner family complete in scoped CODE (2026-10-08)

The full reviewed P_EXATT_TEXT plus MAIN_06_TEXT Extra Attack CODE interval
at `18FE:000A..2280` now has 8822 contiguous accepted bytes: ten complete
logical character/shared owners (8781 bytes) and the existing 41-byte
generic object. The largest 1150-byte Yumemi renderer, 518-byte Chiyuri
beam renderer, and 470-byte Ellen update are included.

The Ellen source is natural `src/main/player/exatt_ellen.cpp`; pinned TC4
compiled all 1078 original executable bytes and correct symbol/fixup
targets, but used a 1024-byte LEDATA boundary that reordered the late
SE-call relocation (owner offset 1003) ahead of the earlier sites.
The documented `scripts/lib/tc4_omf_bridge.py` changes only valid Intel
OMF LEDATA/FIXUPP record framing, at owner offset 1000, and rebases the
three remaining record-local offsets. It emits no bytecode, does not
change code/data storage or symbol targets, and cannot be generalized
without its strict input assertions and negative controls. This is an
explicit producer-layout calibration, **not** a claim that historical
uncalibrated TC4 or TASM emitted identical OMF records.

First passing no-candidate default aggregate:
`.analysis/th03-main-exact/gpt-web-ellen-omf-default-p01-20261008/receipt.json`.
Both cold links match all 320 functions, 50126 function bytes / 51049
owned bytes, all ordered MZ relocations and MAP contributions, 20 product
hashes and DOS behavior. The physical global storage and full MAIN build
closure remain open; OP, MAINL, and ZUN still require stored/decoded CODE
mapping before exact reconstruction.

## Latest full reviewed-CODE acceptance after Ellen (2026-10-08)

The authoritative post-ledger **no-candidate** two-round replay is:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-ellen-omf-default-final-p02-20261008

Receipt: .analysis/th03-main-exact/gpt-web-ellen-omf-default-final-p02-20261008/receipt.json

Both rounds pass all **320 currently reviewed** MAIN functions, 50126 function
bytes / 51049 owned CODE bytes, 72 owned extents and 65 source owners.
The 1078-byte Ellen CODE span matches the immutable target byte-for-byte,
all 14 original ordered MZ relocations, MAP, existing owners, two complete
cold object/output vectors and maintained DOS behavior. Snapshot source
hashes for source, manifest, Oracle, OMF calibration bridge and ledgers
were independently checked against the live worktree.

The Ellen source is natural C++, but the native TC4 object is not claimed
historically exact at the OMF-record level. A narrow fail-closed OMF
LEDATA/FIXUPP framing correction preserves exact instructions and relocation
targets while restoring their original link order. The native and
calibrated object SHA-256 values are independently retained in the receipt.

Full CI attempt: .analysis/th03-ellen-omf-ci-final-20261008.log
(**635 tests, 125 errors importing the absent host unicorn module,
167 skips; full CI FAIL**). The post-unittest gates pass independently
at .analysis/th03-ellen-omf-postgates-final-20261008.log,
including toolchain, target, Ghidra and negative controls. This is
not complete MAIN source-product closure, historical DATA/BSS ownership
or independently pristine target provenance; OP, MAINL and ZUN exactness
remain unresolved. Factory Truth Kernel acceptance is not implied.

## New exact MAIN_010 Hyper/character-state owner

The full 595-byte, ten near-Pascal-callback Hyper dispatcher at target
0D7F0..0DA43 / TLINK 096E:4110..4363 has now been rebuilt from natural
Turbo C++ 4.02 source. The compiler emits **unmodified native OMF**.
Critical ABI details are a MAIN_01 code-group declaration, 1-byte packing
for historical player_stuff_t (shot_mode at +0x0D and hyper callback at
+0x64), and BYTE alignment of the residual frozen carrier after the
odd-length TC4 object. Earlier ungrouped and inaccurate-structure-layout
trials are preserved as negative controls, not accepted as exact.

The scoped native-TC4 default two-round result is:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-hyper-main010-default-final-p02-20261008

Receipt:
.analysis/th03-main-exact/gpt-web-hyper-main010-default-final-p02-20261008/receipt.json

Both rounds passed all 595 linked bytes, original MAP, all four **ordered**
MZ sites, previously accepted 320 functions, object/output vectors and
maintained DOS behavior. The accepted total is now 330 reviewed functions /
50721 function-body bytes / 51644 owned CODE bytes, 73 reviewed extents
and 66 maintained owners. There was no Hyper-specific OMF normalization
or machine-code byte patch. Details and failed experiments are recorded
in docs/reconstruction/MAIN_HYPER_DISPATCH_REVIEW.md.

The post-ledger final receipt is PASS and was checked against the current
source, manifest and evidence/progress hashes. Full CI executed 638 tests but
is blocked on the host's absent `unicorn` dependency (125 import errors,
167 skipped); .analysis/th03-hyper-ci-20261008.log preserves that failure.
The independently runnable post-unittest gates all PASS at
.analysis/th03-hyper-postgates-20261008.log, including target, toolchain,
Ghidra, negative controls, tracking and compile checks. No full CI PASS is
claimed and the repository Oracle is not Factory Truth Kernel acceptance.

The next target-first intake is now **four remaining provisional, non-exact
intervals totaling 3609 bytes**, independently replayable with:

    python3 scripts/review_th03_main_next_frontier.py

The current v2 review is in docs/reconstruction/MAIN_NEXT_FRONTIER_REVIEW.md.
Priority is the two adjacent **843- and 635-byte HUD state/renderer blocks**
as a complete subsystem, followed by the **1958-byte Marisa charge/hyper/
hitbox prefix**, with the 173-byte ordinary-shot producer kept in its
larger dependency chain. The historical v1 five-interval review is
preserved; Hyper must not be counted as unreviewed again. No new exact
credit is assigned to those four intervals until original complete
function boundaries, DATA/BSS and ABI ownership, source and two full
serial cold links are proved. The full MAIN game and OP/MAINL/ZUN remain
incomplete; Factory Truth Kernel acceptance is not implied.
