# TH03 reconstruction handoff

Reconstruction resumed on 2026-10-07 after the historical 2026-10-06 closeout.
This remains an incomplete, verified repository state: the reviewed MAIN authored
frontier advanced, but a complete maintained game build and the 505-file intake
are unfinished. See CLOSEOUT.md for the earlier frozen snapshot.

## Preserved state

| Artifact | Preserved reviewed result | Acceptance |
| --- | --- | --- |
| MAIN | 39 source owners, 46 CODE extents, 120 functions, 14953 owned bytes | Scoped repository-local exact |
| OP | 40 reviewed decoded units / 12386 bytes; 33 source-present extents / 12019 bytes | exact0 |
| MAINL | 145 decoded rows; 34 source-present extents / 3073 bytes | exact0 |
| ZUN | 18 rows; three source-present wrapper TUs / 234 bytes | exact0 |

MAIN's 14953 bytes comprise 14747 function bytes and 206 explicitly classified
producer/table/alignment bytes. The latest accepted full-owner aggregate is
.analysis/th03-main-exact/gpt-web-enemy-promoted-final-20261007/receipt.json.
It passes two fresh compilations/links and the maintained DOS behavior probes
with 20 product outputs, 355 game objects and 421 validated generated OMF objects.
The complete enemy owner is now exact: three extents / 19 functions / 3325 bytes.
A consecutive two-producer reconstruction split reproduces the previously failing
ordered ENEMY_2_TEXT relocation list without changing CODE bytes or weakening the
comparison. Historical source filenames remain unknown; see
reconstruction/MAIN_ENEMY_REVIEW.md.

MAIN_05_TEXT character bombs remain outside the exact aggregate, but the
producer blocker is now experimentally isolated. The complete Ellen
contribution has maintained natural C++ in src/main/player/bomb_ellen.cpp:
TC4J emits the target's exact 1023-byte 280/163/580 function partition and all
347 instruction offset/size/mnemonic shapes. A full MAIN link places this C++
producer exactly at 183C:01EB..05E9 and reproduces Ellen's target 15-entry MZ
relocation order while preserving the complete 71-site owner multiset. A
five-way TASM split does not reproduce that order, so TC4J producer/FIXUPP
behavior, not object boundaries alone, is now proven material. The mixed link
has only 22 Ellen byte mismatches; every one is a DS-relative high byte shifted
by +0x43 because the 0x84-byte private BSS lands at DGROUP:68DC instead of the
target 25DC (+0x4300). The remaining Ellen blocker is therefore physical BSS
placement. The retained object probe is
.analysis/th03-main-bomb-ellen-cpp/gpt-web-ellen-main05-v2-20261007/receipt.json;
the mixed-link diagnostic is
.analysis/th03-main-bombs-split-probe/ellen-cpp-review-v5.json. No exact credit
is claimed yet; recover the four remaining TC4J character producers and
historical DATA/BSS boundaries next. See reconstruction/MAIN_BOMBS_REVIEW.md.

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
database before new target observations. Continue MAIN by reviewing additional
root code/data ownership and the maintained build graph; do not treat the 100%
reviewed-authored frontier as whole-product completion.

Historical closeout CI was 607 tests / 50.517 seconds with available private
headless gates passing at the 2026-10-06 snapshot. Current preflight tracking is 250 units / 2363 evidence rows / three
hypotheses / 295 knowledge rows / 127 MAIN authored-function rows; the accepted
exact subset remains 120 functions.

The current Factory host no longer has the historical Conda Python/Unicorn
installation. The latest /usr/bin/python3 CI attempt runs 610 tests but reports
125 errors, all from missing Python module unicorn, with 167 skips; its log is
.analysis/th03-main-exact/gpt-web-bombs-tc4-proof-checkpoint-20261007/ci.log.
No local wheel, egg, apt cache, or alternate Python with Unicorn is present.
The remaining CI steps were rerun individually and pass: compileall, tracking,
progress, MAINL intake policy, TH03 inventory, target verification, Oracle smoke,
toolchain and analysis-toolchain attestations, TH03-MAIN Ghidra database check,
Ghidra negative controls, and git diff --check. This is an explicit host
dependency block, not a full-CI PASS.
