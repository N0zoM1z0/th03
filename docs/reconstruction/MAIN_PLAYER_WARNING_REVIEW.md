# MAIN warning/HUD source milestone

2026-10-19: source-present only. Seven complete natural functions cover original
load C7A5..CDBD, 1,560 CODE bytes. Accepted MAIN remains 78 exact extents /
371 functions / 59,624 bytes across 70 semantic source owners. Reviewed source
scope becomes 83 extents / 398 functions / 65,232 bytes. No full-link, cold,
runtime, whole-tail or Factory acceptance is implied.

## Actual retained-link four-call checkpoint (2026-10-20)

Source-present only; accepted MAIN remains 81 exact extents / 378 functions / 60,688
bytes. Four warning calls now express the original argument push followed by
NOP, PUSH CS and a real near call to the unchanged far-return callee. Two HUD
calls preserve 6A00/6A01; two palette calls preserve FF76FD and the BP-3 byte PID.
No header, type, storage, prologue, other body or shared-phase changes.

The fresh maintained-path warning object is
`.analysis/gpt-dots-player-tail-retained-probe-v05/run-first-v01/source/obj/th03/warning.obj`
(SHA256 5a1e39d9f20455f5b329dbcfe57f64cba9f5a978e09e73ab27ba98559a33549b).
It retains 1,560 CODE bytes, 125 fixups, 37 literal segment sites in original order,
seven publics and zero storage. The first schema prediction failed because
TC++ emitted exact four self-relative target-frame56 OFFSET16 calls, rather
than the TASM-root group-frame16 form. That failure is preserved unchanged;
no object normalization or accept-either gate was introduced.

The separately reviewed v06 link-only diagnostic reused that object unchanged.
Actual calls at CA61/CA68/CC46/CCD6 are 900EE82BF0/900EE824F0/900EE85DD7/900EE8CDD6,
resolving to BA91/BA91/A3A8/A3A8. All 3,433 contiguous tail bytes now equal the
original target, with full 1,553/owned 83/outside 1,470 literal order, all outside
raw bytes, accepted score/bomb/root, header and overlay preserved. Receipt:
`.analysis/gpt-dots-player-tail-retained-probe-v06/run-first-v01/receipt.json`.
Independent audit: `.analysis/gpt-dots-player-tail-linked-independent-v01/report.json`,
attributing completed command f3d1cea0aa9f4acc82c2911a5ae34e3d.

The original v06 receipt remains HOLD_FULL_MAP for complete zero-contribution
and public-tie display order; a separate supplement does not rewrite it.
Earlier four projected linker lowerings are not evidence of actual lowering:
v04 observed all four still FAR. The explicit source calls above now have actual
linked-byte proof. No cold/runtime/Factory acceptance, ledger status promotion,
whole-original global interposition or exactness credit follows from this
source checkpoint. Historical failed roots, schemas and native runs stay intact.

## Source layout and ABI

`src/main/player/warning.cpp` is one coherent translation unit; warning.hpp
retains the strict byte-PID, packed-player and field-width assertions. The
research one-TU wrapper included warning_early.cpp then warning_state.cpp.
Maintained source flattens those bodies in exactly that order and removes only
the repeated header/codeseg framing and obsolete research comments. The CPP
uses an explicit root-qualified maintained-header path. The header
remains byte-identical; its research label records provenance. No body tuning,
ABI, storage, flags or compiler-profile changes accompany this layout change.
The first maintained-layout probe-v07 failed because this pinned compiler
invocation did not resolve the sibling warning.hpp include. Later diagnostics
were cascades; guards and cleanup passed. The milestone-v01 source freeze and failed
receipt remain intact. Milestone-v02 changes only that include to
"src/main/player/warning.hpp"; the header and all bodies remain unchanged.
Corrected maintained-layout probe-v08 succeeded with all seven lengths and
1,560 CODE bytes. The full independent original-target audit confirms all
125 fixups, 81 branches, register windows and 37-site prediction. LEDATA, FIXUPP,
SEGDEF, EXTDEF, PUBDEF and GRPDEF payloads equal v06. The unused zero-size
default segment name changes from P_WARN_TEXT to WARNING_TEXT; module and
dependency metadata also differ. Whole-object identity is not claimed. This direct
maintained-path compile uses the existing -I. profile and unchanged flags.
Receipt: `.analysis/gpt-dots-tail-warning-probe-v08/compile-first-v01/receipt.json`,
SHA256 2ef199d5ececff0205ea07578573ebc94e48ea61a142c94bab9f9426605fa916.
Object SHA256 67197a27bb95516f2322c218cc516544fc480c71c74de0db03158df8ff4cd02a.
Audit: `.analysis/gpt-dots-tail-warning-independent-review-v08/audit.py`,
SHA256 d7c9ec813f371409bba5c9f76baded04729881c0b598d573e9d461dbe7eaef35.
Result: `.analysis/gpt-dots-tail-warning-independent-review-v08/report.json`,
SHA256 5e503ce624ec0f5153f7bd101f92432f38349cce16b76c852e02ccebe6c1f64d.
Failure receipt: `.analysis/gpt-dots-tail-warning-probe-v07/compile-first-v01/receipt.json`,
SHA256 77c151b689701b1c7b38e0392d98475b70af94cb24f2019f3332185c1274520b.

| Entry | Bytes | ABI |
| --- | ---: | --- |
| C7A5 pause | 139 | near, no arguments |
| C830 highlights | 148 | near, no arguments |
| C8C4 gauge bars | 314 | near, no arguments |
| C9FE portrait | 62 | far Pascal byte PID in word slot; RETF 2 |
| CA3C flash | 143 | far, no arguments |
| CACB warning text | 182 | near Pascal byte PID plus word attribute; RET 4 |
| CB81 warning state | 572 | far Pascal byte PID in word slot; RETF 2 |

Candidate physical producer: PLAYER_M_TEXT / MAIN_01, 096E:30C5, file E005.
Identifiers remain semantic proposals. Eight direct round callers, all 81
branches and the shared text digit tail were checked against TH03.

B398 consumes BX=VRAM offset and jumps into shared B37F; it is not a closed
five-byte helper. B3A2 is the EGC copy and restores DS/SI/DI. B3F6 consumes
DX=pixel x/BX=width, preserves SI/DI and clobbers CX. Compiler register variables
express that real boundary; symbolic assembly CALLs introduce no fake stack ABI.
F5C grcg_setcolor preserves CX. Native argument evaluation and each fresh CX
reload were checked, so no phase carries width across B3F6. Word-port blocks
express observed device semantics; original inline-source provenance is unproved.

Existing storage remains external: players DS:65A6, stride 128, charged word +18h,
available word +1Ah, hyper byte +1Eh; warning flags0798; brightness3938;
direction393A; next393C; active2D54; gaugelevel2D56; bosslevel1E3E. Existing
strings079A..07FA, quit65A0, palette-changed65A1, resident1D90, input1A9A,
frame6596 and palette11BA retain their owners. No DATA/BSS is allocated.

The local unsigned-char view preserves existing one-byte warning storage without
changing its global enum. Postfix mutation produces direct byte INC. Brightness
<=0 and ==0 are equivalent for all 256 byte values. Each raw gauge word shifted
right4 lies in 0..4095; local signed RHS casts are value-preserving and every
available-minus-charged difference lies in [-4095,4095], within signed16.
Declaration order changes local layout without initializing or forcing stack bytes.

## Native observations and retained history

The first probe failed three strict layout assertions. Initial intake and review
incorrectly used 65AA (is_hit at players+4) as the players base; this was an
observed-offset subtraction/review miss, not packing failure. Original pointers
at 9821/9830, accepted MAP and maintained CPU declarations establish 65A6/6626.
Only the assertions/report were corrected to 18h/1Ah/1Eh; packing and bodies
were unchanged. The failed receipt and all earlier sources remain immutable.

Successful native experiments emitted 1597, 1584, 1568 and 1560 bytes. The unsigned
state view fixed real signed JL/JGE comparisons and cast-assignment increments.
The genuine register boundary removed forced local spills; signed width
subtraction removed the final two accumulator round-trips. Text fall-through,
unsigned zero test and local declaration order then matched the target.

Combined probe-v06 emits all seven target sizes, natural LEDATA 1024+536, zero
DATA/BSS and 125 fixups (77 data, 7 near external, 41 far). All 1,560 bytes compare
after valid symbol binding and four genuine same-group far-call lowerings; all
81 branches and register windows agree. The 37 predicted surviving MZ sites
match original literal sites/order (36 early, sole late CCCA) at required C7A5
placement. This is a diagnostic prediction, not an actual linked output.

A runtime staging bug recursively copied historical proof inputs. The corrected
driver materializes only the current dependency closure while guarding historical
bytes/modes in place. State probe-v04 captured 313 files / 30,206,468 bytes and
checked 57,290 historical guard-only files before and after. Historical evidence
was not deleted. See the durable bounded-staging rule in RE_WORKFLOW.

## Evidence and remaining gates

- Frozen combined source: `.analysis/gpt-dots-tail-warning-source-v05/manifest.json`.
- Compile: `.analysis/gpt-dots-tail-warning-probe-v06/compile-first-v01/receipt.json`,
  SHA256 7b5b4339ff6111d8ad729f6783be58209a24b8ca48cb4cf6c36e9297f01a8ff4.
- Native object SHA256 a1c1eadbb6b975ba4585ad39e59b159798104da5b07f663128afda8e41fea775.
- Independent audit: `.analysis/gpt-dots-tail-warning-independent-review-v06/audit.py`.
- Audit result: `.analysis/gpt-dots-tail-warning-independent-review-v06/report.json`.
- Audit review: `.analysis/gpt-dots-tail-warning-independent-review-v06/REVIEW.md`.
- Separate full comparison: `.analysis/gpt-dots-tail-warning-compare-v06/comparison.json`,
  SHA256 a797c58f93cbff031cd378a4b77fac023b5b5f476f8e10ddfea0e6069c915652.
- Source/layout proposal: `.analysis/gpt-dots-tail-warning-milestone-v02/source-freeze.json`.

Generation commands in historical scratch reports are historical only. Never
rerun writers over frozen reports/disassembly; regeneration uses a new location.
No target arrays, padding, fabricated stack ABI, object surgery or FIXUPP rewrite
was used. Current default exact manifests/build remain unchanged. Actual retained
link, full outside preservation, literal linker order, maintained-layout cold
replay and runtime/device behavior remain gates. Under the current CPU/root placement strategy, recovering the whole
3887-byte player tail remains the planned route to remove that ordering cycle.
This cohort has not completed the independent exact-acceptance gates.
