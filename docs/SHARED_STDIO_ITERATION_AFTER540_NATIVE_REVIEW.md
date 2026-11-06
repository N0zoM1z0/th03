# Shared stdio iteration: literal order after540

The existing `flushall` and `xfflush` members now reproduce all five literal
ordered relocation fields as well as their complete 139 initialized CODE bytes.
This is refinement of two existing runtime owners. New member, CODE-extent,
authored-function and whole-product acceptance credit remain zero.

Live sources are `src/shared/crt/flush_all.asm` and
`src/shared/crt/flush_exit.asm`. They use the unchanged bounded
`src/mainl/crt/stdio_layout.inc`. Frozen historical `src/mainl/crt/flushall.asm`
and `xfflush.asm` remain unchanged ancestor inputs. Named stack slots preserve
the original 16-bit locals; FILE stride is 20 bytes and open flags are mask 3.

## Complete original scopes

The comparison independently opens installed TC4 `CL.LIB`, SHA-256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
It does not use a reconstructed carrier as an original. Japanese product targets
retain pinned `candidate-local-attested` provenance; independent pristine-dump
attestation is unknown.

| Original member / slot | CODE | DATA / BSS | Literal field sites, in order |
| --- | ---: | ---: | --- |
| flushall / 223 | 76 | 0 / 0 | +44, +25, +14 |
| xfflush / 335 | 63 | 0 / 0 | +38, +19 |

All fields retain complete original geometry, segment-relative status, frame,
target method/index and addend. Both FAR calls use frame method 5, target method
2 and the original `_fflush` import. Stream-table and stream-count offsets retain
DGROUP frame method 1 and their original import indices. The complete emitted
lists are directly equal in order; sorting never supplies that equality.

The emitted source spans are loop then entry for xfflush (23–62, 0–22), and
loop, stream setup, entry/count setup for flushall (29–75, 19–28, 0–18).
Bounded ORG directives retain record chronology; ordinary instructions cover
every original initialized byte once. There is no filler, target instruction
array, output patch or extra public helper. Original compiler textual source
order is not claimed.

The review checks complete CODE/DATA/BSS extents and initialization coverage;
segment attributes 28h/48h/48h; raw PUBLIC payload/order; literal imports;
GROUP DATA/BSS membership/order; ALIAS and MODEND records. There are no CODE
holes. OMF data-record packing differs, so original OMF-program identity is false.

## ABI and behavior

Both far no-argument entries retain BP frames, SI/DI saves and caller stack
geometry. Far FILE arguments push segment then offset and remove both words.
ES remains subject to the original LES/callee behavior; no new preservation is
invented. The same complete instructions also retain all error paths.

xfflush initializes its remaining count to four and visits exactly those first
four FILE slots, independent of `_nfile`. It calls fflush only when the slot's
read/write flag mask is nonzero and ignores its result.

flushall loads the original 16-bit `_nfile` and retains the unchecked
postdecrement test. Its return counts open slots visited even if fflush fails.
The original pointer-offset increment, 16-bit wrapping and far segment handling
remain unchanged; no defensive domain checks or successful-flush interpretation
are added. Complete native equality resolves this scope without a runtime matrix.

## Affected native product proof

Parent after539 root SHA-256 is
`60a004666a3c62043147feb86d97f2f1231b406070bc150fa794ed9d4d47b095`.
Only the two changed members are assembled. Native TLIB retains all 893 slots
and 891 other member programs unchanged. Source C0, all current game objects
and the validated OP cold pair are reused.

Two native rounds each retain seven complete raw outputs: both OBJ files, LIB,
MAINL EXE/MAP and OP EXE/MAP. All seven repeat byte-for-byte. Eleven successful
native phases and their writer logs remain. Both affected products link the
actual source-generated C0 and rebuilt library through explicit response files.
The reviewer independently reconstructs those responses and checks native argv.

| Output | Result |
| --- | --- |
| MAINL EXE | 67,372 bytes; complete original equality; 677 ordered MZ entries |
| OP EXE | 63,866 bytes; complete original equality; 607 ordered MZ entries |
| MAINL MAP | 80,967 bytes; complete after539 equality |
| OP MAP | 68,078 bytes; complete after539 and historical cold MAP equality |

The original selected runtime storage and native MAP ownership are rechecked
for both products. The earlier actual two-round packed OP proof is reused through
the unchanged decoded input and tool identities. No new DIET run is represented.
The OP-selected diagnostic is now 60 literal-equal streams and 16 order-only
streams; all 76 retain equal per-site fields and import order. These counts do
not increase source/function acceptance. C0's 58-field ordering question and
formal MAINL 0/250 acceptance remain open.

Root: `.analysis/work/runtime-after540-build.json`, SHA-256
`568fed759f13881ea179eb3d874afaa49e1c1ae5b8022c78ebf5dbebf4bb776a`.
Producer/reviewer: `scripts/build_th03_runtime_after540_work.py` and
`scripts/review_th03_runtime_after540_work.py`; recipe:
`config/th03_runtime_after540.json`.

All fourteen raw outputs and eleven logs use `runtime-after540-*`.
The independent review transcript is `runtime-after540-independent-review.txt`.
Consumed sources, include, config, driver, extracted objects and both response
pairs remain in `TH03ML/probe/af540b` and `TH03OP/probe/af540b`. The successful
af540a local probe and its eleven pinned source/object/recipe/log/scope files
remain under its manifest. Displays were empty, writers serialized, one CPU at
nice10. No full CI, cold replay, game-object recompilation, ancestor runtime
chain or output cleanup occurred.
