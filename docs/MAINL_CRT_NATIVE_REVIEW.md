# MAINL CRT source ownership

This review accepts six existing complete CRT producers and two DATA owners:
8 extents, 13 procedures or ABI entries, 628 CODE +93 DATA bytes. These are
library bytes, not authored game code. Previous 164 owners remain unchanged.
The complete maintained source is already part of the current cold graph;
this review adds ownership without changing native inputs or rebuilding them.

## Actual source, library and layout

All six source TUs and the errno/map includes are checked against their actual
`owned/` staging inputs. Their entire current native objects match both retained
cold vectors. The existing two-round cold pair has 938 identical raw outputs.
The normal 893-member library retains every original member position and all
untouched contextual members. Each of the six replaced member's complete
program-record stream equals its actual source-produced standalone object.
THEADR and TLIB bookkeeping supply no instructions or initialized state.

The containing native BYTE CODE/WORD DATA/BSS segments, literal DGROUP membership
order, empty BSS, public aliases and both MAP public tables are checked. All
39 native fields resolve independently against the actual MAP. Complete linked
bytes and literal empty MZ subvectors match the pinned Japanese decoded target.
The full source/tool/cold graph is also revalidated by current acceptance.
No source, object or executable is patched. No full cold, DIET or ancestor
runtime replay is required for these unchanged producers.

| Producer | CODE | DATA | Procedures or ABI entries |
| --- | ---: | ---: | ---: |
| h_llsh | 33 | 0 | 2 |
| h_padd | 96 | 0 | 4 |
| ioerror | 82 | 91 | 2 |
| n_pcmp | 33 | 0 | 1 |
| fbrk | 352 | 2 | 3 |
| setblock | 32 | 0 | 1 |

## Near/far register helpers

N_LXLSH@ has a three-byte near shim that pops the near return, pushes CS and
pushes the offset back, then falls into the 30-byte far body. F_LXLSH@ and
LXLSH@ alias that body. The shift preserves the actual CL mutation and original
CPU shift-count behavior; do not replace it with a host-language shift rule.

The 96-byte pointer bank similarly has two three-byte near shims and two far
bodies of 44/46 bytes. Plain and F_ labels alias the same far entries. Negative
deltas cross-enter the opposite magnitude path, so the physical bodies share
control flow. Three near shims and three far bodies are six distinct callable
entries with disjoint physical ownership; far aliases add no entries or bytes.
N_PCMP@ normalizes low-nibble offsets, wraps segment additions and returns CPU
flags. It does not return a synthesized integer comparison result.

## Heap-break and DOS error chain

The 352-byte fbrk TU contains a private 142-byte grow helper with near `RET 4`,
near cdecl brk of 67 bytes and near cdecl sbrk of 143 bytes. The cached granule
is one zero WORD at DATA:1130. Keep 1-KiB granules, 16-bit rounding, the signed
increment check, negative increments and huge-pointer normalization. Failed
growth updates heap top from DOS's reply while retaining the prior break.

The actual native fbrk object emits an ordinary five-byte far call and a genuine
FAR-pointer field for setblock. The existing real TLINK output naturally turns
it into `NOP / PUSH CS / near CALL` at CODE:3EBC, targeting 8E5A. The comparison
resolves that field; no source NOP or modified object supplies the byte.

setblock is far cdecl and invokes DOS 4Ah. Its failure path saves BX around the
near IOERROR call, then returns that original BX value in AX. FFFF means success;
a failure reporting BX=FFFF collides with the same sentinel. Preserve this
original unchecked contract. IOERROR and DOSERROR are near callee-pop-2 APIs;
DOSERROR returns its original argument after updating error state. The signed
INT_MIN negation and invalid-error-87 fallback also remain unchanged.

The 91-byte error DATA contribution owns the zero doserrno WORD and 89 named
DOS error 0..88 mappings. Every errno equate agrees with the pinned installed
ERRNO.H; the semantic map emits every entry in order. Its two real public
aliases and native DATA bytes are checked. This is a typed error map, not code
or a target-byte array. No BSS gains file-byte credit.

## Evidence and remaining work

`scripts/lib/decoded_mainl_crt_native.py` checks the unchanged current objects,
normal library, MAP and retained cold pair. The bounded receipt is
`.analysis/work/mainl-crt-native.json`; its scope is included in the current
MAINL publication. No physical DOS execution or whole-product source ownership
is claimed. Existing runtime observations remain historical supporting evidence.

The separate MAIN check confirmed the 417-byte input body is exact and the
following EC2D byte still differs (target 90, current 00). No source alignment
directive was added without provenance. Target/current MZ header sizes are
6240/7680 bytes and relocation table offsets are 28/62; the 1553 relocation
entries agree. Those linker/header questions remain open and add no credit here.
