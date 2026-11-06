# Shared DOS path and command tail after542

The existing fullpath and doscmd members now reproduce all 23 literal ordered
relocation fields, both raw PUBLIC packets and all 1,145 initialized CODE bytes.
This refines existing runtime owners. New member, CODE-extent and authored-function
credit remain zero.

Live sources are `src/shared/crt/path_canonicalize.asm` and
`src/shared/crt/dos_command_tail.asm`. Historical `src/mainl/crt/fullpath.asm`
and `doscmd.asm` remain unchanged ancestor inputs. There are no new includes,
private DATA or BSS contributions.

## Original input and complete scopes

The producer independently opens real installed TC4 CL.LIB, SHA-256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
A reconstructed carrier is not used as an original. Product inputs remain pinned
Japanese `candidate-local-attested` targets; independent pristine-dump provenance
is unknown.

| Original member / slot | CODE | PUBLIC entry | Ordered field sites |
| --- | ---: | --- | --- |
| fullpath / 235 | 834 | __fullpath at 89 | 821,798,787,732,693,661,626,536,518,357,269,253,235,190,167,143,102,65 |
| doscmd / 342 | 311 | __DOSCMD at 0 | 227,165,99,66,28 |

All 22 FAR-call fields retain TARGET frame method 5 and EXTDEF target method 2.
fullpath +143 retains its 16-bit DGROUP frame method 1, EXTDEF index 1 and addend
1 (`__ctype + 1`). Every location geometry, segment-relative bit, frame, target
index/method and addend agrees directly in the original literal order. Import
order remains unchanged. No emitted list is sorted to supply ordered equality.

The review also checks complete initialized bytes and segment extents/attributes,
GROUP/ALIAS/MODEND, ordered PUBLIC entries and raw PUBDEF packets. Both publics
are group 0, CODE segment 1, type index 0. There are no extra helper exports.

## Source layout and native coverage

The original is_separator helper stays at 0–30, followed by the near callee-pop8
is_sbcs_separator helper at 31–88. The public fullpath body spans 89–833.
Source keeps both helper addresses and original RET2/RET8 contracts. Its ordinary
logical statement spans emit in the original fixup chronology; forward helper
and public labels retain their actual addresses and types.

doscmd emits its argument-copy/termination span, allocated-prefix setup,
allocation test, argument-size loop and entry in that order. The original
memory layout remains 0–310; its entry is near and returns with RET12.

The native CODE record spans are retained in each scope receipt. The reviewer
checks that their union is exactly the original extent and that every byte is
written once: no holes, duplicate writes or overlapping records. There is no
padding, target instruction array or object/output patch. Native TASM produces
all instructions and relocation records. Original textual statement order and
compiler identity are not claimed. LEDATA/FIXUPP record packing differs, so
complete original OMF-program identity remains false.

The af542a baseline compiles the unchanged historical source with native listing
output. It verifies the existing original bytes and per-site field attributes,
while retaining its unequal literal field order. Listings bind the new semantic
source boundaries to actual native addresses. af542b verifies both new complete
members, ordered fields, PUBLIC entries and one-write CODE coverage. These probes
resolve layout questions and add no source/function credit.

## Preserved original behavior

fullpath retains its far C ABI, 18-byte local frame, SI/DI saves and 161-byte
temporary allocation. Explicit drive recognition, default-drive/current-directory
selection, slash/backslash handling and DBCS boundary checks remain unchanged.
Single-dot reduction, parent traversal and the drive-root failure path retain
their actual helper calls. Character copying keeps 16-bit offset-only pointer
increments and unchecked copy behavior. Caller-buffer size checking, temporary
release, realloc and failure returns preserve the original ownership policy;
no new cleanup or input validation is added.

doscmd retains three far arguments under its near callee-cleanup ABI and a
14-byte local frame. It counts argv strings even when copying is disabled.
The third pointer's presence controls argument copying; its pointed-to contents
are unused. Optional prefix copying, spaces, CR/NUL termination and the leading
length byte remain original. Allocation arithmetic wraps at 16 bits and length
storage at 8 bits; no new DOS-length cap or defensive check is introduced.
Complete native equality resolves these behaviors without a new runtime matrix.

## Two-product native proof

Parent after541 root SHA-256 is
`1799436476f816e7b921ce29997343c2f08d64b5a3f73c5153d87c68117ecdce`.
Only these two members are assembled. Native TLIB retains all 893 slots and
891 other programs unchanged. Source C0, unchanged game objects and the validated
OP cold pair are reused.

Each of two rounds retains seven whole raw outputs: both OBJ files, LIB and
MAINL/OP EXE/MAP pairs. All seven repeat byte-for-byte. Eleven successful native
phases/logs remain. The independent reviewer checks actual source/tool bindings,
native argv, reconstructed C0/library responses and selected material ownership.

| Output | Result |
| --- | --- |
| MAINL EXE | 67,372 bytes; complete original equality; 677 ordered MZ entries |
| OP EXE | 63,866 bytes; complete original equality; 607 ordered MZ entries |
| MAINL MAP | 80,967 bytes; complete after541 equality |
| OP MAP | 68,078 bytes; complete after541 and historical cold MAP equality |

Earlier actual two-round packed OP proofs are reused through unchanged decoded
bytes and pinned tools; no new DIET run is represented. The selected OP diagnostic
now has 64 literal-equal streams and 12 order-only gaps. C0's 58-field order,
formal MAINL 0/250 acceptance and the unknown whole-game denominator remain open.
These diagnostic counts do not increase source/function acceptance.

Root: `.analysis/work/runtime-after542-build.json`, SHA-256
`fee3d18425d239420999d2c8771c28c10310df7225a50f927fbabb29ae8c8c08`.
Producer/reviewer: `scripts/build_th03_runtime_after542_work.py` and
`scripts/review_th03_runtime_after542_work.py`; recipe:
`config/th03_runtime_after542.json`.

All fourteen raw outputs/eleven logs use `runtime-after542-*`. Independent review
transcript: `runtime-after542-independent-review.txt`. Source, driver, config,
extracted objects and MAINL response pairs remain in `TH03ML/probe/af542c`;
OP's consumed C0/library/responses and outputs remain in `TH03OP/probe/af542c`.
af542a/b listings, native objects, source-layout recipe and scope proofs remain
under `.analysis/work/probe/path542/manifest.json` (25 pinned files). Displays
were empty, writers serialized, one CPU at nice10. No full CI, cold replay,
game-object recompilation, ancestor runtime chain or native cleanup occurred.
