# TH03 — current agent handoff (2026-11-06; shared runtime after541)

**Start with this file and actual Git state.** Latest working native evidence:
**after541**; latest independently applied storage audit: **after520**.
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
| Latest closed literal-order gaps | **fflush + fseek: all eight fields ordered-equal** |
| MAINL decoded EXE / ordered MZ relocations | **67,372 bytes / 677; original raw equality** |
| MAINL MAP | **80,967 bytes; two reviewed zero-BSS changes from after537** |
| OP decoded EXE / ordered MZ relocations | **63,866 bytes / 607; original raw equality** |
| OP canonical packed file | **36,041 bytes; original proof reused from after537** |
| OP MAP | **68,078 bytes; complete historical cold MAP raw equality** |
| Formal Factory MAINL canonical unit acceptance | **0/250, unchanged** |

Library totals are not authored-game credit or a whole-game denominator. The
current MAIN ledger has 106 units / 459 authored functions all marked exact;
that is not proof of the unknown whole-game denominator. Do not repeat closed
units as missing source.

Latest root: `.analysis/work/runtime-after541-build.json`.
SHA-256: `1799436476f816e7b921ce29997343c2f08d64b5a3f73c5153d87c68117ecdce`.
Producer/reviewer: `scripts/build_th03_runtime_after541_work.py` and
`scripts/review_th03_runtime_after541_work.py`.
See the [stdio IO/position review](SHARED_STDIO_IO_AFTER541_NATIVE_REVIEW.md).

Live owners are **`src/shared/crt/flush_stream.asm`** (fflush: 209 CODE, TASM)
and **`src/shared/crt/stream_position.asm`** (fseek: 492 CODE, pinned compatible
JWasm), with unchanged bounded `src/mainl/crt/stdio_layout.inc`. All 701 initialized
bytes and eight full ordered fields agree with real CL.LIB; all far/near ABIs,
FILE state, short-write policy, text LF accounting and append seek/restore paths
remain original. There are no CODE holes or extra public helpers. Source uses
ordinary bounded instruction spans, no padding/target arrays/output patches.

Original ordered PUBLIC entries also agree. fseek emits `_fseek` at 137 then
`_ftell` at 267 in one PUBDEF packet instead of two; both raw lists are retained
and this packing difference is explicit. Do not claim original OMF-program or
packet identity, or sort PUBLIC entries/fields. Four explicit WORD comparisons
retain the original AX encodings. The private helper remains PRIVATE. Earlier
TASM trials with reversed PUBLIC order and the first JWasm AX-encoding trial
were rejected; preserve all af541a–e probes and their 40-file manifest at
`.analysis/work/probe/stdio541/manifest.json`.

Both seven-file native rounds repeat (two OBJ/LIB and both EXE/MAP pairs).
The other 891 programs/all 893 slots and both complete after540 MAPs are unchanged;
both decoded EXEs remain original-exact. Packing proof is reused; no game-object,
cold or runtime replay ran. New member/CODE-extent and authored-function credit:
**zero**. All fourteen raw outputs/eleven logs use `runtime-after541-*`; actual
source/include/profile/config/driver remain in `TH03ML/probe/af541f`; OP's
consumed C0/library/responses/outputs remain in `TH03OP/probe/af541f`.

Retained stdio-iteration parent: `.analysis/work/runtime-after540-build.json`, SHA
`568fed759f13881ea179eb3d874afaa49e1c1ae5b8022c78ebf5dbebf4bb776a`.
Live owners `flush_all.asm` and `flush_exit.asm` retain 139 CODE bytes/five ordered
fields; xfflush visits exactly four slots and flushall counts open slots visited
regardless of individual fflush failure. All fourteen raw outputs, eleven logs,
af540b inputs and successful af540a probe remain. See the
[iteration review](SHARED_STDIO_ITERATION_AFTER540_NATIVE_REVIEW.md).

Retained abort parent: `.analysis/work/runtime-after539-build.json`, SHA-256
`60a004666a3c62043147feb86d97f2f1231b406070bc150fa794ed9d4d47b095`.
Its live owner is **`src/shared/crt/abort.asm`**: all 20 CODE bytes, full far ABI,
SI/DI saves and both literal fields (+13 then +7) agree with original CL.LIB.
Both six-file native rounds and nine logs remain; all 892 other programs are
unchanged. Retain af539i inputs and af539a–h probes, including the rejected C
candidates (41-file `.analysis/work/probe/abort539/manifest.json`). See the
[abort review](SHARED_ABORT_AFTER539_NATIVE_REVIEW.md). Do not repeat those
failed C/register-ABI probes or replace the original library with a carrier.

Retained near-frame parent: `.analysis/work/runtime-after538-build.json`.
SHA-256: `7647b0fdf6bc43c769d526422cad48907d1e58c0d31260766b0a7936f61cbb07`.
Producer/reviewer: `scripts/build_th03_runtime_after538_work.py` and
`scripts/review_th03_runtime_after538_work.py`.
See the [near-frame/native MAP review](SHARED_RUNTIME_NEAR_FRAMES_AFTER538_NATIVE_REVIEW.md).

The five live refined owners in `src/shared/crt/` are `heap_break.asm`,
`dos_write.asm`, `execl.asm`, `load_program.asm`, `dos_resize.asm`. The first
four use pinned compatible JWasm; setblock retains TASM and its correct original
CODE frame0. All 1,648 existing CODE / 42 DATA bytes and 77 complete per-site
literal fields agree with real original CL.LIB. All import orders, public
ownership, GROUP and segment attributes agree. Ten near frames and setblock's
GROUP are corrected; **zero new member/CODE-extent credit**. execl's two fields
and setblock's one field are ordered-equal; fbrk/write/loadprog still have order
gaps. Private helpers remain PRIVATE: the first diagnostic candidate's extra
helper exports were rejected and preserved, not adopted.

Both ten-file native rounds repeat. All 888 other source programs and 893 slots
are unchanged. MAINL/OP whole EXEs remain original-exact; OP's complete MAP now
also equals its original cold MAP. MAINL's MAP differs from after537 only by
removing zero-sized fbrk BSS at 0E3F:2872 and adding zero-sized setblock BSS at
0E3F:2880; every material row and other byte is equal. The two actual after537
packed OP proofs are reused; no new packing run is represented. No game object,
native cold graph or ancestor runtime model is rebuilt.

All twenty raw outputs and seventeen native logs use `runtime-after538-*`.
Actual sources, includes, recipe/profile and response pairs remain in both
`TH03ML/probe/af538l` and `TH03OP/probe/af538l`. All bounded probes af538a–k,
failed candidates, raw outputs, sources and logs remain. No cleanup ran.

Retained shared-exec / first OP bridge root: `.analysis/work/runtime-after537-build.json`.
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

Prioritize actual selected-runtime order gaps, not unlinked library counts.
The current retained diagnostic is
`.analysis/work/runtime-after541-selected-literal-field-audit.json` / `.txt`.
All 76 selected OP members now have identical raw per-site field attributes:
62 literal streams are equal, 14 differ only in order. This is an investigation
queue, not source credit. The order-only members are atexit, dosenv,
exit, ioerror, xxv, fbrk, signal, fullpath, setvbuf,
write, xalloc, xmsg, doscmd and loadprog. C0's 58-field order also stays
open. Never sort an emitted list and then call it literal ordered equality.

The stdio flush/position pair is now closed. Continue an actual selected scope,
for example fullpath (slot 235: 834 CODE, 18 fields) or doscmd (311 CODE, 5 fields),
after inspecting the real original and its complete ABI/ownership boundaries.
These are existing owners, not missing functions or whole-game progress counts.

ioerror slot 79 has 82 CODE/91 DATA and five fields in order 22,28,45,39,51, but
its original PUBLIC stream interleaves CODE0, DATA2, DATA0, CODE62. Inspect that full
stream before attempting a replacement; sorted-by-segment publics hide a real
ordering question. Its original BSS/DATA GROUP remains intentional. Preserve
frozen `src/mainl/crt/ioerror_link.asm` and the after536 parent proof.

Extend **after541**, retaining all after537–540 live shared refinements and C0.
Call the latest reviewer once; it validates the complete unchanged source DAG,
not ancestor runtime chains. All historical TUs/recipes remain frozen; use new
bounded shared owners as needed. Earlier 893-slot totals and partial bosses are
not missing-source queues or whole-game percentages.

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

After537's OP MAP had two zero-BSS row differences; after538's OP MAP is now
raw-equal to the historical cold MAP. The current MAINL zero-BSS row review is
recorded above; material ownership and all other bytes remain unchanged. Do not overwrite historical MAPs or demand
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
PYTHONPATH=scripts nice -n 10 taskset -c 0 .venv/bin/python scripts/review_th03_runtime_after541_work.py
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
filename is not an evidence-deletion oracle. Current af537–541 and all failed
branches remain. Routine cache cleanup does not authorize touching these files.
