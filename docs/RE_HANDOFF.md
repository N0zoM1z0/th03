# TH03 agent handoff — after575 source-native follow-on (2026-11-06)

The earlier after554 handoff was written before reconstruction resumed. That
archive accurately had no after555 native build at the time. This repository
now contains independently verified, retained after555–after558 and after566 MAINL
source-native stages and after559–after565 MAIN source-native stages.
Formal decoded publication/Factory acceptance has not been silently repinned;
the after554 publication baseline below remains historically valid. The original
source checkpoint before this follow-on was
`e7697e1` (`gpt-web: recover MAINL registration and ending data banks`). Later
handoff commits change documentation/storage only; nothing has been pushed.

## Newly verified after566 source-native stages (not new Factory credit)

- MAIN: after559 Chiyuri (11 complete functions / 2,654 CODE bytes) and
  after561 the other eight major bosses (74 functions / 14,797 CODE bytes).
  Every original 16-bit TC4 object matches after timestamp-only normalization.
  All eight were also rebuilt in two independent rounds and substituted
  simultaneously in the normal MAIN link. Including Chiyuri, this covers
  nine major bosses / 85 functions / 17,451 CODE bytes; these were existing
  source owners, so the ledger function denominator is unchanged.
- MAIN: after565 natural TASM keyboard scanner fixes the only remaining
  load-image byte at EC2D through an assembler EVEN, not a codestring or
  target-byte patch. Two native OBJ/EXE/MAP rounds now reproduce **all
  124,642 original Japanese MAIN load-image bytes and all 1,553 ordered
  MZ relocation entries**. The original MZ file *header* remains different
  (390 vs480 paragraphs, relocation table offsets 28 vs62); the full
  original EXE file is not accepted.
- MAINL: after555 formula-driven atan/sin table DATA896, after556
  maintained 1,859-byte root DATA scope, after557 two complete far vector
  functions (159 CODE plus one natural EVEN), and after558 four C/C++ sound
  functions (124 instruction bytes +4 historical codestring tails).
  The old after549 input scanner's adjacent 90h byte is now also solved
  in after566 through true native TASM EVEN. This separately proves
  the complete MAINL 418-byte held-key CODE producer; both native rounds
  reproduce all 67,372 decoded original EXE bytes and all 677 ordered
  relocations without cold replay. These are bounded source evidences,
  not a new canonical MAINL publication.
- Current source-native MAIN last receipt:
  .analysis/work/main-input-after565-native-build.json.
  Current review: scripts/review_th03_main_input_after565_work.py.
  Existing after561 eight-boss source root:
  .analysis/work/main-eight-boss-after561-native-build.json.
  MAINL last new stage:
  .analysis/work/mainl-input-after566-native-build.json.
  Read-only review: scripts/review_th03_mainl_input_after566_work.py.
  Preserve the full raw receipt DAG and both complete native rounds;
  old after520/after554 storage audits do not authorize cleanup of these.

## Source-derived MAIN original DOS MZ file (after568)

The normal after567 dual 99-object TLINK builds, with nine source-native
boss objects and the natural TASM input scanner simultaneously linked,
reproduce all 124,642 Japanese original MAIN program bytes and all 1,553
original ordered MZ relocation entries. They retain a newer TLINK
132,322-byte file header (480 paragraphs / relocation table at decimal 62)
instead of the original compact MZ 130,882-byte file header (390
paragraphs / table at decimal 28).

After568 includes a **separate standard DOS MZ format serializer**, not
a new linker or a target-byte repair. It obtains all fourteen original
native MZ header values, all original source-generated relocations and
the unmodified program image from each of the two native after567
outputs. With a minimal 28-byte fixed DOS header and 1,553 records,
the relocation region is exactly 6,240 bytes, requiring no alignment
padding. Each independent result is the complete exact **130,882-byte
Japanese original EXE**, SHA-256 f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b.

The negative control confirms the same format conversion does not
fix the old wrong EC2D input CODE byte. This proves reproducible
source-derived original file bytes, **not** original linker tool
provenance, source ownership of every program byte, or formal Factory
product acceptance. The direct TLINK EXE remains retained and distinct.
Keep both original link outputs, compact outputs, the read-only
verification and parent source/OBJ receipts:
  .analysis/work/main-combined-after567-native-build.json
  .analysis/work/main-compact-after568-native-build.json
  scripts/review_th03_main_compact_mz_after568_work.py

## MAINL original registration initialized DATA alignment (after569)

The old after554 source-bound registration source intentionally ended at
303 initialized bytes. Original regpre.obj also initialized DATA+303 to 00h,
which after554 was supplied by linker alignment rather than a source.
The new alternative maintained registration_even.asm compiles with ordinary
TASM EVEN at that final odd offset. Two source-native TASM/TLINK rounds
recreate the complete 304-byte original context payload, all two literal
ordered OMF fixups and 35 PUBLIC names/positions. The resulting entire
67,372-byte Japanese MAINL decoded EXE and all 677 relocations remain
original-exact; only the registration MAP contribution size changes from
012F to 0130 compared with the earlier 303-byte source link.

The old registration.asm and all old source-bound acceptance receipts
remain byte-unchanged, so nothing silently repins the historical after554
publication. One native DATA alignment byte is a source-backed layout
contribution, not a newly discovered instruction, extra authored function,
or additional original game code credit. Native parent root:
  .analysis/work/mainl-register-even-after569-native-build.json
  scripts/review_th03_mainl_registration_even_after569_work.py

## Source-backed large enemy script and collision C++ (after572)

The four original enemy producer objects can now be recompiled, twice,
from small genuine Turbo C++ wrapper translation units that all include
one unchanged maintained src/main/enemy/enemy.cpp source. This covers
3,325 complete original CODE bytes, 19 functions and 222 ordered native
OMF fields, including the 867-byte enemy_run script interpreter and
848-byte enemy_hittest collision controller.

Each 4-object native group is simultaneously linked with the after567
nine major BOSS and natural keyboard source objects, preserving the
entire 124,642-byte Japanese program image, all 1,553 original MZ
relocations, and the complete selected 132,322-byte native linker file.
The separate after568 compact DOS MZ format step still reconstructs
both exact original 130,882-byte Japanese EXEs without target-byte
patches. Original OMF THEADR/LNAMES/COMENT packets differ due to wrapper
source filenames, and the 19 authored functions were already counted in
the historical ledger. No canonical acceptance, new function credit or
original historical compiler source identity is inferred.

Latest evidence:
  .analysis/work/main-enemy-four-after572-native-build.json
  scripts/review_th03_main_enemy_four_after572_work.py
  docs/MAIN_ENEMY_SHARED_CPP_AFTER572_NATIVE_REVIEW.md

## MAINL large cutscene plus source-natural sound (after573)

An independent first-use GAME=3/BINARY=L Turbo C++ translation unit now
includes the unchanged maintained 573-line cutscene script interpreter
and drawing controller. Two targeted native compiler/TLINK rounds each
reproduce the original complete 3,195-byte CODE allocation, all
13 original near procedure PUBLICs, 236 ordered OMF relocation fields,
the 56 in-scope MZ relocation sites and the *entire 67,372-byte
Japanese decoded MAINL EXE* with all 677 ordered relocations.
This source-native link uses the after570 four natural sound TASM
routines and after569 registration DATA/input/VECTOR/root/C0 parents.

Cutscene was already source-reviewed and accepted before this new link,
so no extra authored function count, duplicate source credit or
canonical Factory unit is claimed. The independent first-use C++ object
differs in source-module diagnostic OMF headers/COMENT bookkeeping, not
initialized CODE, public/function layouts or literal field chronology.

  .analysis/work/mainl-cutscene-after573-native-build.json
  scripts/review_th03_mainl_cutscene_after573_work.py

## MAINL large Staff Roll source C++ integration (after575)

Both independently source-compiled original Turbo C++ Staff Roll/ending
producer objects now match the complete 3,695 CODE + 224 initialized
DATA bytes, all 342 ordered OMF fixups, 19 original code PUBLIC
procedures and six DATA PUBLIC symbols. Replacing only staffdat.obj in
the after573 cutscene/sound/input/registration source-native link yields
both complete 67,372-byte Japanese decoded MAINL EXEs and all 677
relocations original-equal, preserving all original MAP offsets.

The first after574 native attempt had a too-strict cross-round MAP text
comparison (the *upstream cutscene* was intentionally named r1/r2).
That stage's exact native scripts, objects, logs and unfinished report
are retained as a negative evidence branch. A fresh after575 stage
correctly compares original MAPs plus bounded filenames and passed both
source-native rounds. No historic source receipt or Factory acceptance
is silently repinned; the nineteen procedures are already accounted.

  .analysis/work/mainl-staff-after575-native-build.json
  scripts/review_th03_mainl_staff_after575_work.py

## Start here

Read [AGENTS.md](../AGENTS.md), [workflow](RE_WORKFLOW.md),
[architecture](ARCHITECTURE.md) and the local `th03-re` skill. Use existing private
inputs/tools and `.venv`; run preflight at session start/environment changes.
Japanese provenance is `candidate-local-attested`; independent pristine-dump
identity and whole-game source/function denominators remain unknown.

Keep original unchecked behavior, 16-bit ABI/storage and native link order.
No padding, instruction-byte arrays or object patches to manufacture equality.
Historical consumed TUs/recipes stay frozen. Use bounded `.inl` includes and
local dependencies/explicit `compat/rec98` forwarding. Empty DISPLAY/WAYLAND,
one allowed CPU at nice10, and serialize Wine/Borland writers with the existing
`.analysis/borland-wine-writer.lock`. Preserve the Wine prefix and tool identities.

## Current verified evidence

| Scope | Current result |
| --- | --- |
| MAINL selected native link | after554; root552, picture C table553 and text banks554 |
| MAINL reviewed decoded source | **220 extents / 290 procedures / 37,968 bytes** |
| MAINL source byte partition | 34,431 CODE + 3,531 initialized DATA + 6 file-backed uninitialized DATA |
| MAINL source origins | 17,717 authored / 20,251 library bytes |
| MAINL decoded EXE / ordered MZ relocations | **67,372 bytes / 677; entire original raw equality** |
| MAINL MAP | 81,039 bytes; after554 differs from553 only in registration DATA304→303 |
| MAINL formal canonical Factory acceptance | **0/250**, separate from decoded source scopes |
| Shared compiler library | **893/893 source-bound slots / 209,272 CODE-extent bytes**, including unlinked members |
| Selected MAINL / OP runtime material | 75 / 76 members; library totals are not authored-game credit |
| OP decoded EXE / relocations / packed file | 63,866 bytes / 607 / 36,041 bytes; original equality retained |

Other product accounting is in [generated progress](PROGRESS.md). MAIN's106
ledger units /459 authored functions do not prove a whole-game denominator.

Current MAINL root: `.analysis/work/text-banks-after554-native-build.json`.
SHA-256: `e498f16501b5b4d1c0f56a73fb65e4c87af607502da12b21730fd1a6eedafd89`.
Review: `.analysis/work/text-banks-after554-native-review.json`, SHA-256
`d7a8583e90631b29b009046b6fae68c9469bd9560e6525c3026c36540a90c642`.
Its two raw two-OBJ/EXE/MAP vectors and six writer logs remain in place.
Actual consumed sources/responses are in `TH03ML/probe/af554b`.

**Future MAINL links retain all four prior source objects**: both after554 text
bank OBJs, after553 picture OBJ and after552 root OBJ. Also reuse the actual
source C0 and unchanged library references in `rounds[i].reused`, rather than
historical default helpers pointing to after535. Shared-runtime root is
`.analysis/work/runtime-after548-build.json`, SHA-256
`b0bed460844c39c51a1496b312ac0b94120cfff2ccd7e202e6abdb01db9ed773`.
All earlier source-bound parent rounds/logs remain active dependencies.

## Exactness limits and open questions

- C0: all58 literal ordered fields agree; all32 PUBLIC packet/definition sets
  agree, but their emitted order remains open. Keep native TASM, entry and frames.
- `setvbuf`: bytes/per-site fields agree; two MOV operand pairs still differ in
  literal fixup order. Do not repeat the documented compiler/assembler variants.
- MAINL input: the historical after549 held-key scan captured 417
  instructions and42 ordered fields but lacked the following90h alignment
  byte; its product candidate was unaccepted. The after566 maintained
  forwarding TU uses the natural source-ordered 8086 body and native TASM
  EVEN to own all 418 CODE bytes. Both after566 whole EXE/ordered-
  relocation rounds now match. Original OMF packet field order differs
  from the Turbo C++ object, so original OBJ identity remains unclaimed;
  formal publication is still the older after554 scope.
- Sound wrappers: natural no-codestring controls emit29/57/27/11 bytes,
  each one shorter than its target contribution. After558 reproduces
  the four complete historical C/C++ objects but still counts their four
  explicit codestring tails as unproved function bytes. Vector's old
  alignment ambiguity is closed by native TASM EVEN in after557.
- Ownership audit:716 project CODE-allocation bytes across9 contributions remain
  outside publication. DATA queue:1864 bytes in contextual `th03_mainl.asm` plus
  one registration trailing byte. Tables, alignment and BSS are not missing
  function counts. Root552's typed BSS186 already exists and gets no file credit.
- MAIN: the old after554 retained candidate had one differing load-image
  byte at EC2D (90 versus00). After565 closes that source gap with native
  TASM EVEN; only the original MZ header size/relocation offset differs.
  TLINK `/i` did not close it.
  Private TLINK2.0 under DOSBox reports29 fixup overflows; its partial output is
  rejected. Earlier AX0006 was a bridge error, not proof of OMF incompatibility.

The historical after554 registration source omits one final initialized
word-alignment 00h, previously supplied by TLINK at0E3F:0A5D. After569
rebuilds that byte with a natural TASM EVEN in a separate maintained source,
while preserving the original after554 publication and source byte hashes.
All117 bank PUBLIC definitions/packet sets agree, but eight ending digit-alias
PUBLIC packets still differ in order. Do not claim original compiler/assembler
identity or duplicate old DATA/registration acceptance credit.

The original interrupted [after555 research](AFTER555_UNBUILT_RESEARCH.md)
was an unbuilt handoff; independent, tested after555–after558 native
source stages have since superseded its hypotheses. The original research
remains safely archived at `.analysis/handoff/after555-unbuilt/`, with15 exact draft files and a
SHA-256 manifest. It includes readable root DATA and a binary-independent trig
formula generator. **All proposed extents/counts remain unbuilt hypotheses.**

## Proportionate checks

```sh
.venv/bin/python scripts/preflight.py
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_text_banks_work.py
.venv/bin/python scripts/audit_th03_mainl_ownership_gaps.py --check
.venv/bin/python scripts/validate_tracking.py
.venv/bin/python scripts/progress.py --check
git diff --check
```

Choose an allowed CPU and nice10 wrapper as shown in the workflow. The latest
scoped review validates actual retained source/native inputs without cold
rebuild or ancestor runtime suites. Do not call old runtime-review chains as
routine gates: one reaches an obsolete live211 publication check. The root552
preservation check binds2178 frozen native inputs to after548 Git; it explicitly
handles the untouched `src/main/player/bombs.inl` CRLF checkout. Do not normalize
that file or repin historical receipts during cleanup.

## Storage and detailed references

Read [current storage policy/results](STORAGE_HANDOFF_CURRENT.md). The applied
native-deletion audit remains the historical after520 prefix; it rejects this
newer checkout. **No native outputs were deleted during this handoff.** Cache
cleanup and Git `--no-prune` repacking reclaimed approximately64.4 MiB while
preserving all17,363 pre-existing Git objects and all12,785 private work files.
This work-file inventory is not a newly certified active source DAG.

Keep the complete raw parent DAG, all diagnostic manifests, Japanese targets,
tools and reference archives. No general unreferenced/age-based sweep. Commit
substantial work as `gpt-web: xxx`; do not push without a request.

Latest bounded reviews: [text/state554](MAINL_TEXT_BANKS_AFTER554_NATIVE_REVIEW.md),
[picture table553](MAINL_PICTURE_FILES_AFTER553_NATIVE_REVIEW.md),
[root552](MAINL_ROOT_STATE_AFTER552_NATIVE_REVIEW.md),
[switch tables551](MAINL_SWITCH_TABLES_AFTER551_NATIVE_REVIEW.md),
[completion550](MAINL_COMPLETION_AFTER550_NATIVE_REVIEW.md),
[input candidate549](MAINL_INPUT_SCAN_AFTER549_NATIVE_REVIEW.md),
[startup548](SHARED_STARTUP_AFTER548_NATIVE_REVIEW.md).
Earlier roots/ABI/storage caveats are retained in the
[after554 handoff archive](RE_HANDOFF_ARCHIVE_AFTER554.md); use the current file
for present state, rather than copying an archived “current” claim.
