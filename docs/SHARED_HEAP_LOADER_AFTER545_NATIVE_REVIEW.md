# Shared heap break and program loader after545

Two existing selected runtime members now reproduce 1,223 CODE bytes,
42 initialized DATA bytes and all 65 literal ordered relocation fields.
Both have zero BSS. This refines existing source owners; new member,
CODE-extent and authored-function credit remain zero.

## Complete original members

The original is the independently opened installed TC4 CL.LIB, SHA-256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
Japanese targets retain `candidate-local-attested` provenance; independent
pristine-dump attestation remains unknown. Reconstructed carriers are not
used as originals.

| Member / slot | Live owner in src/shared/crt | CODE | DATA | Fields |
| --- | --- | ---: | ---: | ---: |
| fbrk / 167 | heap_resize.asm | 352 | 2 | 33 |
| loadprog / 891 | program_loader.asm | 871 | 40 | 32 |

All original bytes, segment geometry/attributes, import order, GROUP,
ALIAS/MODEND and public ownership agree. Complete field geometry,
segment-relative status, frame, target method/index and addend agree directly
in emitted order, without sorting. Original CODE site sequences are:

| Member | Original and native sites, in order |
| --- | --- |
| fbrk | 311,308,302,293,289,283,280,276,266,257,254,229,225,218,181,172,168,162,153,149,128,124,119,111,108,98,77,74,64,54,47,36,16 |
| loadprog | 855,844,792,779,768,754,712,709,691,680,667,651,633,601,580,562,558,510,476,442,424,414,380,358,317,245,228,198,189,168,152,30 |

Ordinary instruction spans preserve the native record chronology. All actual
branch/procedure labels are bound before span emission, preserving exact
displacements and near/far distances. Every initialized byte is emitted once,
without holes or overlaps; no padding, instruction-byte arrays or output
patches supply equality. Both owners use the pinned compatible JWasm profile;
loadprog retains the unchanged bounded `crt_errno.inc`. Original compiler
identity and textual source order are not claimed. Historical after538
`heap_break.asm`/`load_program.asm` remain unchanged ancestor inputs.

## ABI, storage and behavior

fbrk retains near cdecl public entries `__brk` at 142 and `__sbrk` at 209,
plus the private near RET4 growth helper. Its initialized word granule cache
remains DATA. Unsigned16 rounding, DOS paragraph clamping, normalized huge
pointer comparisons and signed32 upper-bound behavior remain unchanged.
Negative increments still undergo original normalization. A failed resize
updates heap top from the DOS reply while leaving the break unchanged; the
original BX=FFFFh collision with the setblock wrapper's success value remains.
No defensive bounds or overflow checks are added.

loadprog retains near cdecl `__LoadProg` at 269 and two private far helpers.
The loader's 156-byte frame and probe's unchecked 80-byte candidate remain.
DBCS delimiter scanning, offset-only pointer increments, drive/separator
handling, explicit extension and COM/EXE/BAT search order, COMSPEC lookup and
40 bytes of named static strings are preserved. It keeps the near DOSCMD and
DOSENV calls with their original callee cleanup, command-length check, errno
stores, near execution callback, raw environment allocation ownership and
deferred argument-stack cleanup. No truncation or pointer checks are added.

All three ordered PUBLIC entries agree, including group/segment/frame,
name/offset/type-index. loadprog's raw PUBLIC packet agrees. fbrk's original
two same-CODE records pack into one native record; both full packet lists and
the explicit false packing-equality result remain in the receipts. Complete
original OMF-program identity is not claimed.

## Affected native product proof

Parent after544 root SHA-256 is
`5382d231ccf9cc1ae3f59b365524277b5e983ba7d5f2dba2b82f21ff7c3cd087`.
Only these two owners are assembled. Native TLIB preserves all 893 ordered
slots and 891 other member programs. Source C0, unchanged game objects and
the validated actual OP cold pair are reused.

Two rounds each retain seven complete raw outputs: both OBJ files, LIB,
MAINL EXE/MAP and OP EXE/MAP. All seven repeat byte-for-byte. Eleven successful
native phases/logs remain. The independent reviewer passed, checking consumed
source/include/profile/tool bindings, native argv, independently reconstructed
C0/library responses and selected initialized/uninitialized material ownership.

| Output | Result |
| --- | --- |
| MAINL EXE | 67,372 bytes; complete original equality; 677 ordered MZ entries |
| OP EXE | 63,866 bytes; complete original equality; 607 ordered MZ entries |
| MAINL MAP | 80,967 bytes; complete after544 equality |
| OP MAP | 68,078 bytes; complete after544 and historical cold MAP equality |

Earlier actual packed OP proofs are reused through unchanged decoded bytes
and tool identities. No new DIET run is represented. The selected OP diagnostic
now has 71 literal-equal streams and five order-only gaps: xxv, signal, setvbuf,
xalloc and xmsg. C0's 58-field order, formal MAINL 0/250 acceptance and the
unknown whole-game denominator remain open. These counts are diagnostic only.

Root: `.analysis/work/runtime-after545-build.json`, SHA-256 `74e57df4ccf9f5b92225d7c0c3c8b56b413ca0c298f35056986a2179424d68ca`.
Producer/reviewer: `scripts/build_th03_runtime_after545_work.py` and
`scripts/review_th03_runtime_after545_work.py`; recipe:
`config/th03_runtime_after545.json`.

All fourteen raw outputs/eleven logs use `runtime-after545-*`. Independent
review transcript: `runtime-after545-independent-review.txt`. Actual source,
include/profile/config/driver and MAINL responses remain in `TH03ML/probe/af545c`;
OP's consumed C0/library/responses/outputs remain in `TH03OP/probe/af545c`.
The baseline listings and successful complete-member probes remain in af545a/b,
with their recipes under `.analysis/work/probe/heap-loader545/manifest.json`
(28 files, SHA-256 `47069d345083fd59c90a5e1656e3a8374736e2d987fe7d67ce2d0f402a714d2a`).
Displays were empty, writers serialized, one CPU at nice10. No full CI,
cold replay, game-object compilation, ancestor runtime replay or cleanup ran.
