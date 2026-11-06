# TH03 — current agent handoff (2026-11-06; shared runtime after537)

**Start with this file and actual Git state.** Latest working native evidence:
**after537**; latest independently applied storage audit: **after520**.
The former long handoff remains in
[the historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current source and native evidence

| Evidence | Current |
| --- | ---: |
| Source-bound compiler-library slots | **893/893** |
| Whole-library CODE extents, including unlinked members | **209,272 bytes** |
| Actual MAINL selected runtime members / CODE extent | **75 / 29,961 bytes** |
| Actual OP selected runtime members / CODE extent | **76 / 29,964 bytes** |
| Shared exec source correction | **255 initialized work bytes + four literal frames** |
| exec complete extent / initialized / true holes | **933 / 931 / 2 bytes** |
| exec original literal ordered relocation fields | **21/21 equal** |
| Fresh two-product native output rounds | **2; all seven raw outputs repeat** |
| MAINL decoded EXE / ordered MZ relocations | **67,372 bytes / 677; original raw equality** |
| MAINL MAP | **80,967 bytes; exact after536 equality** |
| OP decoded EXE / ordered MZ relocations | **63,866 bytes / 607; original raw equality** |
| OP canonical packed file | **36,041 bytes; original raw equality** |
| OP MAP | **68,078 bytes; two zero-extent rows explicitly reviewed** |
| Formal Factory MAINL canonical unit acceptance | **0/250, unchanged** |

Library totals are not authored-game credit or a whole-game denominator. The
current MAIN ledger has 106 units / 459 authored functions all marked exact;
that is not proof of the unknown whole-game denominator. Do not repeat closed
units as missing source.

Latest root: `.analysis/work/runtime-after537-build.json`.
SHA-256: `ee5fcbe49af194eab79fe96234fcf23a627e91a114b6d3e2032891b1cdbeab2c`.
Producer: `scripts/build_th03_runtime_after537_work.py`.
Independent reviewer: `scripts/review_th03_runtime_after537_work.py`.
Scope: `config/th03_runtime_after537.json`.
See the [full shared runtime review](SHARED_EXEC_OP_RUNTIME_AFTER537_NATIVE_REVIEW.md).

The latest live exec owner is **`src/shared/crt/dos_exec.asm`**. Its named work
fields recover original LIDATA initialization; only saved-environment bytes
356–357 remain uninitialized. Imported data declarations outside the empty
DATA segment recover original TARGET frame5 at +371,+397,+482,+560. All raw
initialized bytes, segment attributes, GROUP, imports, PUBLIC, MODEND and 21
full ordered fields now agree with the real compiler member. Data-record
packing differs; complete OMF-program identity is not claimed.

**Important original-input correction:** the after338 exec review compared the
28-source carrier (`64b0a5…`), not real installed CL.LIB (`7d53ed…`). Its old
uninitialized-work-area / original-program-identity claims were wrong. Both old
review documents now point to the correction. Preserve all historical receipts
and frozen `src/mainl/crt/exec.asm`; do not edit their hashes or pretend they
were new original-library observations. Always use the actual pinned installed
compiler library independently of any accepted/reconstructed carrier.

After537 assembles only exec and rebuilds its library, retaining **892 other
programs and all 893 positions**. Both targets reuse the source C0 and their
unchanged game objects. OP's current 330-source graph and thirty-object cold
vector are checked; no game object/cold graph is recompiled. Two real native
OP DIET -B/-ra rounds reproduce the stored target and decoded roundtrip. Both
products' selected material segments are checked directly against real CL.LIB,
including initialization coverage, true holes, attributes and MAP ownership.
The compiler/runtime sources are proved common through actual two-product
links; no duplicate authored-function or CODE-extent credit is added.

All seven raw outputs per round and thirteen native logs remain at
`.analysis/work/runtime-after537-*`. Actual consumed source/recipe/config,
extracted objects and both response pairs remain in
`TH03ML/probe/af537d` and `TH03OP/probe/af537d`. The reviewer independently
reconstructs and checks explicit source-C0/library linker responses and their
actual native argv. Earlier af537a/b/c probes remain. The first reviewer and
its result are preserved in `.analysis/work/probe/runtime537-response-review/`;
the current successful transcript is `runtime-after537-independent-review-v2.txt`.
No output cleanup occurred.

## Next bounded work

Prioritize real selected-runtime exactness gaps, not unlinked library counts.
The current diagnostic inventory is
`.analysis/work/runtime-after537-selected-literal-field-audit.json` (and `.txt`).
Among OP's 76 actual members, 56 have equal literal streams, 16 differ in order,
and four have per-site attributes differing from actual original CL.LIB:

- `fbrk`: six near-call frame differences.
- `write`: CODE+23 near `__IOERROR` frame.
- `execl`: CODE+26 near `__LoadProg` frame.
- `loadprog`: CODE+633/+754 near `__DOSCMD` / `__DOSENV` frames.

Those ten fields use original TARGET frame5 versus native CODE frame0. Start
with actual source/import placement and actual original fields; the successful
exec correction shows why putting externs in a segment can create the wrong
frame. Do not assume moving a declaration also preserves emission order: check
all complete ordered fields and raw storage. Keep both native streams literal;
never silently normalize frames or reorder object output. This inventory is an
investigation queue, not added source-exact credit. C0's 58-field order and
ioerror's five-field order also remain open. Earlier unchanged C/alias/two-pass
ioerror attempts did not close its order; do not repeat them without new evidence.

Extend **after537**, not after533/536: those older libraries lose the corrected
exec initialization/frames. Call the latest reviewer once, then read its actual
retained pair. It validates the unchanged source receipt DAG and parent tool /
include / raw-frame bindings without ancestor runtime models. Keep frozen
sources and old recipes intact; use a new bounded owner TU when necessary.

## Required retained parents and reviewed MAP limits

- after536 root: `.analysis/work/mainl-after536-baseline-refinements-build.json`,
  SHA `c2b2853f4bddda4a73e2e01c8a78fe407c6a32e35b0f41ed8a6217f306de831d`.
  `h_padd_link.asm` preserves original ordered PUBLIC payload through pinned
  compatible JWasm; `ioerror_link.asm` matches original GROUP. Native raw
  vectors/logs use af536f paths. Its MAP differs from the old cold MAP only by
  F_PADD@/PADD@ display order at shared 0000:3182 and zero-sized ioerror BSS at
  existing 0E3F:286A. First comparator stop, 21 snapshots and all probes remain.
- after535 C0 root: `.analysis/work/mainl-after535-startup-build.json`, SHA
  `9a3592185b880d53d344cdd3f0cf0c0b13534d186833e7d739f673edd2e61d6b`.
  `src/mainl/startup/c0.asm` is supplier-derived large-model source: 623
  initialized CODE bytes, 2-byte CODE cache, 144 DATA, 128 reserved STACK.
  Its 58 individual fields agree but ordering differs. af535e vectors/logs,
  module-name correction snapshots and failed/probe branches remain.
- after534 traces the earlier four baseline owners. after533 retains the 889
  incremental owners, including all 197 iostream and string/regexp blocks.
  Older cplx2, isteldbl and h_ldiv bosses are already complete source owners;
  their historic partial candidates are not additional missing functions.

OP's new MAP differs from historical OP only by adding zero-sized fbrk BSS at
0D7F:2502 and omitting zero-sized setblock BSS at 0D7F:2510. Every material
row and every other byte agree. Do not overwrite historical MAPs or demand
raw equality to a different reviewed empty-segment/alias enumeration. Neither
MAP is patched or broadly normalized. Source acceptance stays separate from
native output equality; all remaining literal OMF gaps remain explicit.

## Scoped commands and operating rules

```sh
git status -sb
git log -8 --oneline
# At session start / environment or target changes:
.venv/bin/python scripts/preflight.py
# One current review already validates its unchanged parent DAG:
PYTHONPATH=scripts nice -n 10 taskset -c 0 .venv/bin/python scripts/review_th03_runtime_after537_work.py
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
```

Keep displays empty, heavy work on one allowed CPU at nice10, Borland/Wine
writers serialized through the preserved prefix/lock. Use pinned Japanese
`candidate-local-attested` targets. Re-attest a database before use. Preserve
16-bit ABI/segments/x87/order and original unchecked behavior. Use only affected
native builds; no routine full CI, cold replay or ancestor runtime chain.
Commit substantial progress as `gpt-web: xxx`; do not push without instruction.

## Storage protection

The latest applied [after520 audit](STORAGE_HANDOFF_CURRENT.md) protects the
258-stage / 5,760-file source receipt DAG. Its pinned
`scripts/cleanup_mainl_after520_handoff.py` removed only 15 audited superseded
files (1.57 MiB). All after521+ source layers require a fresh source-DAG and
SHA-256 audit before deleting native outputs. Do not apply historical after439,
after388/511-source, 319-source or generic clean_generated deletion previews.
Retain the entire active DAG: both raw OBJ/LIB/EXE/MAP rounds, writer logs,
source/recipe snapshots, originals, targets and tools; age or an unreferenced
filename is not an evidence-deletion oracle. Current af537 and all failed
branches remain. Routine cache cleanup does not authorize touching these files.
