# TH03 final handoff

Reconstruction work stopped at the owner's request on 2026-10-06. No further
reconstruction is queued. This is an incomplete, verified repository snapshot;
a complete maintained game build and the 505-file intake are unfinished.
See [closeout](CLOSEOUT.md) for cleanup and final verification.

## Preserved state

| Artifact | Preserved reviewed result | Acceptance |
| --- | --- | --- |
| MAIN | 38 source owners, 43 CODE extents, 101 functions, 11628 owned bytes | Scoped repository-local exact |
| OP | 40 reviewed decoded units / 12386 bytes; 33 source-present extents / 12019 bytes | exact0 |
| MAINL | 145 decoded rows; 34 source-present extents / 3073 bytes | exact0 |
| ZUN | 18 rows; three source-present wrapper TUs / 234 bytes | exact0 |

MAIN's 11628 bytes comprise 11487 function bytes and 141 producer/table/alignment
bytes. Its latest accepted full-owner aggregate is
`.analysis/th03-main-exact/sol-main-restored-aggregate-20261006/receipt.json`.
Its149unchanged source/input guards remain matched; three later-updated
ledger/progress hashes are historical and predate closeout. The audit records
that drift without rebasing the receipt or claiming a fresh cold aggregate.
The complete enemy candidate remains non-exact: three extents / 19 functions /
3325 bytes, with original ordered ENEMY_2_TEXT relocations failing. See
[enemy review](reconstruction/MAIN_ENEMY_REVIEW.md).

Japanese YUMEZIKU targets remain pinned in `config/targets.toml`, with
candidate-local-attested provenance; independent pristine-dump confirmation
is unknown. Frozen ReC98 revision:
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`. Reference or cross-game exactness
is never inherited. Stored OP/MAINL/ZUN and restored diagnostic namespaces
remain distinct; decoded rows do not invent packed-file offsets.

The intake has 505 files. MAIN has 69 paths with scoped CODE review; MAINL has
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

Product source and Oracle-bearing scripts stay at their attested paths.
Detailed history lives in [bounded notes](reconstruction/README.md), ledgers
and Git; this handoff records final status rather than repeating every probe.
Targets, runtime images, the game-local Wine prefix, Ghidra projects, referenced
proof inputs, cold receipt trees and meaningful failed transcripts are kept.
Retired unreferenced preliminary diagnostics are recorded in the closeout
cleanup receipt; historical fingerprint inventories are not rewritten.

For verification, run `python3 scripts/preflight.py`, focused checks,
`python3 scripts/ci.py` and `git diff --check`. Use headless tools and one
Borland/Wine writer. Re-attest a selected Ghidra database before any new target
observations. New reconstruction would require a separate instruction.

Final closeout CI:607tests /50.517seconds, available private headless gates PASS.
Log `.analysis/closeout/sol-closeout-20261006/ci-final.log`; tracking now
249units/2342evidence/293knowledge/120MAIN authored-function rows.
