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

MAIN_05_TEXT character bombs remain outside the accepted aggregate, but their
CODE reconstruction is now complete enough for formal Oracle integration. All
five physical character producers have maintained natural TC4 C++:
Chiyuri 490 bytes / 169 instructions, Ellen 1023 / 347 across three functions,
Kana 526 / 184, Kotohime 528 / 185, and Rikako 546 / 186. Their full-link CODE
contributions land consecutively at 183C:0001..0C29.

The previous relocation blocker is solved. Restoring TC4's uppercase Pascal OMF
public spelling for the maintained randring AND/MOD getters preserves the
existing exact 120-function aggregate while allowing the Rikako producer to
link naturally. A five-C++-producer MAIN experiment then reproduces every one
of the bomb owner's 71 relocation entries in target order. With private state
still emitted by each C++ object, the only 62 owner-byte differences are
DS-relative operands caused by BSS placement: Ellen 22 bytes, Kana 18,
Kotohime 6 and Rikako 16.

A symbolic storage-binding experiment removes even those differences without
hard-coded addresses: semantic externs are bound to the already-symbolized
monolithic TH03 BSS labels at Ellen 25DC/25DE/265E, Kana 2674, Kotohime 28F6
and Rikako 4B8C. The resulting full MAIN link has 3113/3113 bomb-owner bytes
equal, all 71 relocation sites equal, the 71-entry order equal, and zero
mismatches in all seven functions. Retained evidence:
.analysis/th03-main-bombs-rikako-link-probe-e23/review-storage-bind.json.
This proves the CODE owner model but does not claim the monolithic BSS as
physically reconstructed ownership. Next encode the five producers plus
symbolic storage bindings in the checked-in Oracle, promote the CODE extent if
the two-round aggregate stays green, and keep the historical BSS split as a
separate open ownership task. See reconstruction/MAIN_BOMBS_REVIEW.md.

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
