# Archived after554 handoff before the documentation/storage maintenance

# TH03 — current agent handoff (2026-11-06; MAINL text554 / pictures553 / root552 / shared runtime548)

**Start with this file and actual Git state.** Latest working native evidence:
**after554** (MAINL text banks, retaining pictures553/root552), **after548** (shared runtime/OP); latest independently
applied storage audit: **after520**.
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
| Fresh two-product native output rounds | **2; five fresh outputs repeat + unchanged library pair** |
| Latest closed literal-order gaps | **C0 startup: all 58 fields ordered-equal** |
| Partial setvbuf refinement | **all bytes/per-site fields equal; two MOV pairs still unordered** |
| MAINL decoded EXE / ordered MZ relocations | **67,372 bytes / 677; original raw equality** |
| MAINL MAP | **81,039 bytes; only registration DATA304→303 from after553** |
| OP decoded EXE / ordered MZ relocations | **63,866 bytes / 607; original raw equality** |
| OP canonical packed file | **36,041 bytes; original proof reused from after537** |
| OP MAP | **68,078 bytes; complete historical cold MAP raw equality** |
| MAINL reviewed decoded source scopes | **220 extents / 290 procedures / 37,968 bytes** |
| Formal Factory MAINL canonical unit acceptance | **0/250, unchanged** |

Library totals are not authored-game credit or a whole-game denominator. The
current MAIN ledger has 106 units / 459 authored functions all marked exact;
that is not proof of the unknown whole-game denominator. Do not repeat closed
units as missing source.

Shared runtime root: `.analysis/work/runtime-after548-build.json`.
SHA-256: `b0bed460844c39c51a1496b312ac0b94120cfff2ccd7e202e6abdb01db9ed773`.
Producer/reviewer: `scripts/build_th03_runtime_after548_work.py` and
`scripts/review_th03_runtime_after548_work.py`.
See the [startup review](SHARED_STARTUP_AFTER548_NATIVE_REVIEW.md).

Live C0 owner is **`src/shared/crt/startup_large.asm`**, supplier-derived with
zero authored-game credit. All 58 literal ordered fields, 17 original segments,
623 initialized CODE bytes, two CODE cache holes at 621/622, 144 DATA bytes and
128 reserved STACK bytes agree. Raw THEADR/LNAMES/SEGDEF/GRPDEF/EXTDEF/ALIAS/
MODEND records agree. Native TASM retains original nfile frames and entry.
Every initialized byte is written once; no padding, byte arrays or object patch.

All 32 complete PUBLIC packets/definitions agree as sets, but their original
emitted order remains open, unchanged from the after535 native order. Do not
call that ordered equality or complete OMF identity. JWasm syntax/frame/entry
candidates and native TASM default/explicit /kh probes are preserved in af548a–g,
with 47-file `.analysis/work/probe/startup548/manifest.json`. Historical startup
source and after535 recipe remain frozen.

Only C0 is assembled. Both five-file fresh rounds repeat: startup OBJ and both
products' EXE/MAP. All 893 library members and game objects are unchanged; actual
parent library rounds are reused by reference and checked against native copies,
not counted as new TLIB output. Both original decoded EXEs and complete after547
MAPs agree. Packed OP proof is reused. Ten fresh raw outputs/six writer logs use
`runtime-after548-*`; inputs and MAINL responses remain in `TH03ML/probe/af548h`,
OP's consumed C0/library/responses/outputs in `TH03OP/probe/af548h`.

**Subsequent stages must reuse `rounds[i].outputs.startup` from this after548
root**, plus its unchanged library references. MAINL additionally reuses the
root OBJ from after552, picture C OBJ from after553 and both text-bank OBJs from after554 below. The old helper expression
`base.parent.parent.REPORT` still points to historical after535 and would undo
the startup order refinement. Keep that old pair as baseline evidence.

Retained C++/library parent: `.analysis/work/runtime-after547-build.json`, SHA
`5c834b1fd5f52c4af31f25c63a55edeaa9d6f59054db727f659e5e289c3ba68a`.
Live exception_state/allocation_exception/message_exception owners retain
2,117 CODE/296 DATA bytes, four true BSS bytes and 89 ordered fields. All 32
PUBLIC entries agree; packet counts 25/4, 2/1, 5/1 remain explicitly different.
Keep all sixteen raw outputs/thirteen logs, af547c inputs and 39-file af547a/b
manifest. See the [C++ review](SHARED_CPP_EXCEPTIONS_AFTER547_NATIVE_REVIEW.md).

Retained after546–539 parents remain active source-DAG dependencies. Their
root hashes, ABI/storage details and explicit PUBLIC packing differences are
in the [signal](SHARED_SIGNAL_AFTER546_NATIVE_REVIEW.md),
[heap/loader](SHARED_HEAP_LOADER_AFTER545_NATIVE_REVIEW.md),
[environment/stdio](SHARED_ENVIRONMENT_STDIO_AFTER544_NATIVE_REVIEW.md),
[error/termination](SHARED_ERROR_TERMINATION_AFTER543_NATIVE_REVIEW.md),
[path/command](SHARED_DOS_PATH_COMMAND_AFTER542_NATIVE_REVIEW.md),
[stdio IO](SHARED_STDIO_IO_AFTER541_NATIVE_REVIEW.md),
[iteration](SHARED_STDIO_ITERATION_AFTER540_NATIVE_REVIEW.md) and
[abort](SHARED_ABORT_AFTER539_NATIVE_REVIEW.md) reviews. Keep complete raw pairs,
writer logs, consumed inputs and all diagnostic branches/manifests: af546d,
af545c, af544o, af543c, af542c, af541f, af540b and af539i. Native PUBLIC record
packing differences are not whole-program identity. The private exit engine is
RET6 and DOSENV is near RET12, regardless of old frozen comments. The private
TC101/TC201 candidates remain outside accepted product recipes. Do not repeat
closed source/ABI probes or treat their diagnostic counts as source credit.

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
and setblock's one field are ordered-equal. The former write/fbrk/loadprog
order gaps close in after544/545. Private helpers remain PRIVATE: the first
diagnostic candidate's extra helper exports were rejected and preserved, not adopted.

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

## New input candidate and ownership queue (after549)

The input candidate remains outside the active **after554** exact-output root.
`src/mainl/hardware/input_scan.asm` recovers the complete 417-byte / 115-instruction
MAINL function with all 42 ordered native fields, external state and true RETF
boundary. It uses no register self-assignment or hand-filled trailing NOP.
Two candidate OBJ/EXE/MAP vectors repeat; independent instruction-scope review
passes. Original following byte CD09=90 stays unowned. Omitting it changes later
addresses and yields 323 EXE differences, so no full-product or published credit
is claimed. Historical input_sense.cpp remains frozen in the active cold graph.

Candidate root `.analysis/work/mainl-input-scan-build.json`, SHA
`fb67e160ba2f75e21e13e9252b1e96ac8959f5f45753348ae83d964bb0afde82`.
Producer/reviewer: `build_th03_mainl_input_scan_work.py` /
`review_th03_mainl_input_scan_work.py`. Keep six fresh raw outputs/four logs,
af549h consumed inputs and both actual after548 C0/library references. See the
[input review](MAINL_INPUT_SCAN_AFTER549_NATIVE_REVIEW.md).

The read-only `audit_th03_mainl_ownership_gaps.py --check` now binds all **220**
published owners to target bytes and36 project objects. After551 leaves **716
project CODE-allocation bytes across9 contributions** outside publication
(after550:807/11; after549:905/13). This is not a missing-function count:
input418, sound wrappers128, vector_far160 and ten seam bytes. Prioritize these
concrete questions rather than repeating unchanged runtime metadata.

C0 /ml, TASM setvbuf forward-declaration and isolated TC2.01 ABI probes did not
close the old gaps; retain the 60-file af549a–g diagnostic manifest. The TC201
tool candidate is private, outside product recipes; preflight passed after its
installation. Do not repeat these settings as if they were new evidence.

## Retained project scopes (after550/551)

The [completion review](MAINL_COMPLETION_AFTER550_NATIVE_REVIEW.md) adds two
procedures/98 CODE and40 pointer DATA bytes. Its farheap/setupio source bridges
retain the actual after332/493 pairs and old reports; setupio comment identity
is false. Keep the after550 preservation snapshot and af550a sound probe.

The [switch review](MAINL_SWITCH_TABLES_AFTER551_NATIVE_REVIEW.md) adds90 inline
data bytes plus one demonstrated compiler alignment byte, not new procedures.
The actual `-a2`/`-a1` contrast explains all236 fields/publics and five shifted
near calls. Cutscene3195 partitions as3122 instructions/72 table/1 alignment;
root CODE2458 as2440 instructions/18 table. Preserve af551a's nine source/native
files, three logs, private driver/report and prior-publication snapshot.

## Complete selected MAINL root TU (after552)

Live selected TU: `src/mainl/root/recovered/complete.cpp`, with bounded CFG/win/
state `.inl` inputs. All278 fields and all non-comment cold OMF records agree.
Two normal TCC/TLINK rounds repeat whole OBJ/EXE/MAP; entire original67372-byte
EXE/current80967-byte MAP agree. Reuse35 game objects and actual after548 C0/LIB;
no TLIB, packing or cold replay. DATA112 gains one owner; BSS186 is typed,
reserved beyond file end and gets **zero file-byte credit**. All217 accepted
extents total37,287 bytes, with unchanged290 procedures. See the
[root review](MAINL_ROOT_STATE_AFTER552_NATIVE_REVIEW.md).

Root `.analysis/work/root-state-after552-build.json`, SHA256
`67c1c0c2daf57a684c6cca46098a1a05b1efcc7418c6ba30f0fabd295f58cd83`.
Producer/reviewer: `build_th03_mainl_root_state_work.py` /
`review_th03_mainl_root_state_work.py`. Keep six raw outputs/four writer logs,
af552h source/recipe/response inputs and actual inherited library/startup pairs.
Future MAINL links reuse this root OBJ in addition to after548 C0/LIB.

The old runtime-review chain now fails at its obsolete live211 publication
gate. The new root reviewer instead checks2178 frozen native inputs against
after548 Git plus both actual runtime vectors and the current cold graph. One
untouched CRLF checkout has explicit text-transport hashes; no native bytes are
normalized or historical receipts repinned. af552a's four direct TCC controls
emit29/57/27/11 bytes without manual codestrings: their NOP tails stay unowned.
Keep af552b and the32-file diagnostic manifest under `probe/root552/`.

## Selected MAINL picture filename table (after553)

`src/mainl/root/picture_files.c` supplies the natural nine-entry near-pointer
DATA18 at0E3F:0090. Both complete OBJ/EXE/MAP vectors repeat; whole original
EXE and677 ordered MZ relocations agree. Only this C TU is rebuilt; retain
actual after552 root OBJ, after548 C0/library and34 cold game objects. MAP81039
changes only the explicit empty CODE/DATA/empty BSS contributor rows. Native C
fields descend with DGROUP frame1; old generated ASM fields ascend with frame5.
That OMF difference remains explicit; original-game standalone OBJ is unknown.
All218 accepted extents total37,305 bytes, unchanged290 procedures; no BSS credit.
See the [picture-table review](MAINL_PICTURE_FILES_AFTER553_NATIVE_REVIEW.md).

Current MAINL root `.analysis/work/picture-files-after553-build.json`, SHA256
`1b4c3f0d4d82364afea5d1fb78fdab81b7d9ddd6de3ef4b0bcac88ca4f3a771b`.
Producer/reviewer: `build_th03_mainl_picture_files_work.py` /
`review_th03_mainl_picture_files_work.py`. Preserve six raw outputs/four logs,
af553h inputs and inherited pairs. Keep the149-file private diagnostic manifest
under `probe/after553/`; no cleanup occurred.

MAIN has one differing load-image byte atEC2D(target90/native00), plus an MZ
header-size/relocation-offset difference. Current TLINK `/i` does not close it.
Actual private TLINK2.0 inside headless DOSBox reports29 fixup overflows and
writes FAILED; its partial output has4724 differences and is rejected. Earlier
AX0006 results were bridge errors, not proof of OMF incompatibility. Preserve
`probe/link553/` including all DOS inputs/logs/outputs; do not repeat these flags
or adopt the partial file. No target/header patches or manual tail fill.

## Selected MAINL semantic text/state banks (after554)

`src/mainl/data/registration.asm` and `ending_text.asm` replace generated DATA
context with303+360 maintained bytes and61 readable strings. UTF-8 source is
reversibly staged as CP932/CRLF; the local REGI alphabet preserves all72 sprite
IDs. Four zero hold words and both full ordered near-pointer fields agree.
All117 PUBLIC definitions/packet sets agree; ending's emitted PUBLIC order
still differs and is explicitly retained. No original-game standalone OBJ claim.

Both two-OBJ/EXE/MAP rounds repeat; whole original EXE and677 ordered MZ
relocations agree. MAP81039 differs from after553 only in registration DATA
extent304→303. The historical extra final zero is excluded: current TLINK's
following WORD alignment supplies one zero at0E3F:0A5D, still unowned.
All220 accepted extents total37,968 bytes; procedures stay290. See the
[text/state review](MAINL_TEXT_BANKS_AFTER554_NATIVE_REVIEW.md).

Current root `.analysis/work/text-banks-after554-native-build.json`, SHA256
`e498f16501b5b4d1c0f56a73fb65e4c87af607502da12b21730fd1a6eedafd89`.
Producer/reviewer: `build_th03_mainl_text_banks_work.py` /
`review_th03_mainl_text_banks_work.py`. Retain both new OBJs, actual after553
picture OBJ, after552 root and after548 C0/library;32 cold game objects remain
unchanged. Keep eight fresh outputs/six logs, af554b inputs and the18-file
`probe/text554/manifest.json`. The failed af554a DOS `tasm` launch precedes
all native output; actual TASM32 works directly. No cold replay or cleanup.

The remaining project DATA queue is now1864 bytes within `th03_mainl.asm`, plus
the unowned single registration trailing byte. Recover the former from semantic
declarations/consumers; do not turn the latter into hand-filled source padding.

## Next bounded work

Prioritize the input trailing-byte provenance and concrete project ownership
queue above; retain selected-runtime gaps without inventing library credit.
The current retained diagnostic is
`.analysis/work/runtime-after547-selected-literal-field-audit.json` / `.txt`.
All 76 selected OP members have identical raw per-site field attributes:
75 literal streams are equal; only setvbuf still differs in order. This is an
investigation queue, not source credit. Its two MOVs need an actual native
producer that emits both symbolic fixes in original operand order. Repeating
logical-span scheduling, NASM, the tested BCC45 naked/global forms or TCPP1.01
register flags does not resolve that question; preserve the existing probes.

C0's 58-field order is closed in after548; its 32-entry PUBLIC order remains
open. Native TASM preserves original entry/frames, while the tested JWasm form
changes them. Preserve those exact scopes when investigating another producer;
do not repeat the tested /kh settings as if they solved PUBLIC order. Complete
EXE equality alone does not close startup or whole-product source acceptance.
The selected error/termination, DOS path/command, environment/write, heap/loader,
signal, stdio flush/position and C++ exception scopes now have ordered fields.
Never sort emitted lists to claim literal ordered equality.

The source-ordered PUBLIC-queue method is now proved through actual linked
CODE/DATA interleaving. Preserve record-packing differences explicitly and
prebind backward branch labels before separately scheduled test spans when
needed; require every original byte/field and one-write initialized coverage.
Historical TUs/recipes stay frozen. Extend **after554 for MAINL**, retaining
after548 shared runtime/C0 and all earlier live refinements. These remain existing owners, not missing
functions or whole-game progress counts.
Call the latest root reviewer once; it validates retained source/native inputs
without obsolete live-publication gates or ancestor runtime chains. Use new
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
  Its historical 58-field order differs; the live pair is now after548. af535e
  vectors/logs,
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
# Current MAINL source/native preservation and both selected root rounds:
PYTHONPATH=scripts nice -n 10 taskset -c 0 .venv/bin/python scripts/review_th03_mainl_root_state_work.py
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
filename is not an evidence-deletion oracle. Current af537–543 and all failed
branches remain. Routine cache cleanup does not authorize touching these files.
