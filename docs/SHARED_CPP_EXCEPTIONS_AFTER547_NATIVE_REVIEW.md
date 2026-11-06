# Shared C++ exception runtime after547

Three existing selected members now reproduce all 2,117 CODE bytes,
296 initialized DATA bytes and 89 literal ordered relocation fields.
The four-byte destructor-count pointer remains genuinely uninitialized BSS.
CODE includes original executable bodies, typed unwind records and RTTI;
these totals are not authored-game progress or new source-member credit.

## Complete original scopes

The original is the independently opened installed TC4 CL.LIB, SHA-256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
Japanese targets retain `candidate-local-attested` provenance; independent
pristine-dump attestation remains unknown. Reconstructed carriers do not
supply the original.

| Member / slot | Live owner in src/shared/crt | CODE | DATA | BSS | Fields |
| --- | --- | ---: | ---: | ---: | ---: |
| xxv / 156 | exception_state.asm | 649 | 296 | 4 | 16 |
| xalloc / 336 | allocation_exception.asm | 513 | 0 | 0 | 24 |
| xmsg / 337 | message_exception.asm | 955 | 0 | 0 | 49 |

All original initialized bytes, segment geometry/attributes, import order,
GROUP/ALIAS/MODEND and public ownership agree. All three explicitly declare
original DATA/BSS GROUP order under the pinned compatible JWasm profile.
Historical mainl CRT TUs remain unchanged ancestor inputs. No original
compiler identity or textual source order is claimed.

All complete field geometries, segment-relative flags, frames, target
methods/indices and addends agree directly in emitted order. Complete site
sequences are:

| Member | Original and native CODE sites, in order |
| --- | --- |
| xxv | 612,609,597,389,235,227,222,141,133,130,127,110,80,3; then DATA14,10 |
| xalloc | 487,441,421,394,360,344,287,265,234,230,206,188,161,157,142,139,136,125,113,99,91,64,46,18 |
| xmsg | 927,884,852,810,760,752,717,705,673,652,649,646,635,601,588,584,552,548,533,530,527,512,504,494,474,442,416,394,373,334,326,291,271,254,251,248,237,203,187,166,127,119,88,68,51,48,45,34,0 |

Ordinary instruction/metadata spans retain native record chronology, with
real code, unwind and RTTI labels prebound. Initialized bytes are emitted
exactly once without gaps or overlapping writes. Both 128-byte exception
workspaces remain initialized DATA; the destructor-count pointer remains
uninitialized at all four BSS sites. No padding, instruction-byte arrays,
output patches or sorting of emitted lists manufacture equality. RTTI and
unwind pointers remain genuine symbolic FAR/offset fields.

## Ordered PUBLIC ownership

All 32 ordered PUBLIC entries agree, including group/segment/frame,
name/offset/type-index. xxv's cross-segment queue is recovered explicitly:

1. CODE: both polymorphic-DTC getters, unexpected, terminate, set_unexpected,
   set_terminate, call_terminate, call_unexpected.
2. BSS: DestructorCountPtr.
3. DATA: the original 15 exception-chain, handler, saved-state and buffer globals.
4. CODE: ExceptInit.

The raw packet lists are preserved, with packing differences required
explicitly: xxv packs 25 original records into four, xalloc two into one,
xmsg five into one. None is represented as raw PUBLIC packet equality or
complete original OMF-program identity.

## ABI, storage and behavior

xxv keeps its original near/far call distances and return frames, terminate /
unexpected handler replacement and calls, exception-chain access through SS,
saved DS behavior, catch cleanup and abort paths. Both polymorphic-DTC getters
retain their original near/far vtable layouts. ExceptInit initializes the
original SS-relative runtime state and named process exception globals.

xalloc retains conditional allocation of its six-byte object, base xmsg
construction, stored size word and original destructor-count updates. Its
raise path keeps the on-stack copy, typed xalloc RTTI, base relation, original
40-byte local frame and deferred exception-call argument cleanup. Private
copy/destruction helpers retain their far return ABI and deletion flag behavior.

xmsg retains construction from string, copy construction, destruction, raise
and assignment. Its four-byte handle, owned Borland string, 34-byte exception
frames, self-assignment branch, original allocation paths, destructor-count
bookkeeping and cleanup order remain unchanged. No defensive null/overflow
checks are added. Complete native equality resolves these bounded scopes
without an emulator or input-domain matrix.

af547a retains compatible-writer baseline listings and comparisons. Its GROUP
order differs from the original in all three members. xmsg also emits FFFD
instead of FEB1 for the internal copy-constructor call's displacement at CODE572.
Prebinding the actual copy-constructor label at 239 restores that call; no object
patch supplies the correction. af547b passes all complete original member and
ordered PUBLIC checks. Baseline evidence is preserved as observed.

## Affected native product proof

Parent after546 root SHA-256 is
`8870088a19f3733dbd91f3b3fdc43c102155df7d257215cccad3dc5c3c24ff58`.
Only the three listed owners are assembled. Native TLIB preserves all 893
ordered slots and 890 other member programs. Source C0, unchanged game objects
and the validated actual OP cold pair are reused.

Two rounds each retain eight complete raw outputs: all three OBJ files, LIB,
MAINL EXE/MAP and OP EXE/MAP. All eight repeat byte-for-byte. Thirteen successful
native phases/logs remain. The independent reviewer passed, checking source /
profile/tool bindings, native argv, independently reconstructed C0/library
responses and selected initialized/uninitialized material ownership.

| Output | Result |
| --- | --- |
| MAINL EXE | 67,372 bytes; complete original equality; 677 ordered MZ entries |
| OP EXE | 63,866 bytes; complete original equality; 607 ordered MZ entries |
| MAINL MAP | 80,967 bytes; complete after546 equality |
| OP MAP | 68,078 bytes; complete after546 and historical cold MAP equality |

Earlier actual packed OP proofs are reused through unchanged decoded bytes
and tool identities. No new DIET run is represented. The OP-selected diagnostic
now has 75 literal-equal streams; setvbuf is its sole order-only member, with
two reversed MOV operand pairs. C0's 58-field order, formal MAINL 0/250
acceptance and the unknown whole-game denominator remain open. No new
member/extent/authored-function or whole-product acceptance credit is inferred.

Root: `.analysis/work/runtime-after547-build.json`, SHA-256 `5c834b1fd5f52c4af31f25c63a55edeaa9d6f59054db727f659e5e289c3ba68a`.
Producer/reviewer: `scripts/build_th03_runtime_after547_work.py` and
`scripts/review_th03_runtime_after547_work.py`; recipe:
`config/th03_runtime_after547.json`.

All sixteen raw outputs/thirteen logs use `runtime-after547-*`. Independent
review transcript: `runtime-after547-independent-review.txt`. Actual source /
profile/config/driver and MAINL responses remain in `TH03ML/probe/af547c`; OP's
consumed C0/library/responses/outputs remain in `TH03OP/probe/af547c`. af547a/b
probes, comparisons, layouts and recipe scripts remain in the 39-file
`.analysis/work/probe/cpp-exceptions547/manifest.json`, SHA-256
`73046e398b2942d08638b1d38fad2e5b7da4b0a3e7458fa7eac5e950a165ca7e`.
Displays were empty, writers serialized, one CPU at nice10. No full CI,
cold replay, game-object compilation, ancestor runtime replay or cleanup ran.
