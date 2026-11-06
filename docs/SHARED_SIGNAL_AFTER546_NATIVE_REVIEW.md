# Shared signal runtime after546

The existing selected signal member now reproduces all 769 CODE bytes,
38 initialized DATA bytes and 55 literal ordered relocation fields. Its
four-byte saved interrupt vector remains genuinely uninitialized BSS.
This refines an existing owner, adding no member, CODE-extent or authored
function credit. Whole-product source acceptance remains false.

## Complete original scope

The original is slot 180, signal, in the independently opened installed TC4
CL.LIB, SHA-256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
Japanese product targets retain `candidate-local-attested` provenance;
independent pristine-dump attestation remains unknown. A reconstructed carrier
does not supply the original.

Live owner: `src/shared/crt/signal_dispatch.asm`, using the pinned compatible
JWasm profile without includes. Historical `src/mainl/crt/signal.asm` remains
an unchanged ancestor input. All original segment geometry/attributes, import
order, GROUP/ALIAS/MODEND and public ownership agree. GROUP member order is
explicitly BSS, DATA, matching both the original and actual after545 member.

All 55 complete field geometries, segment-relative flags, frames, target
methods/indices and addends match directly in emitted order. The complete
CODE site sequence is:

```text
10,21,24,73,79,124,135,138,187,193,239,251,254,303,309,366,
402,421,464,468,66,180,296,315,319,326,409,411,415,417,442,
513,520,523,540,544,579,599,699,717,489,493,503,527,549,553,
568,572,587,591,656,660,733,739,748
```

Both MOV operand pairs, `(409,411)` and `(415,417)`, naturally retain their
original internal fixup order. They differ from setvbuf's still-open reversed
operand pairs. Ordinary instruction spans preserve the rest of the native
record chronology, with all actual branch/API labels bound first. Every
initialized CODE/DATA byte is emitted once, without gaps or overlapping writes.
All four BSS sites remain uninitialized. No padding, instruction-byte arrays,
object patches or sorted emitted lists manufacture equality.

The original ordered PUBLIC entries are `_raise` at CODE618, then `_signal`
at CODE392. All group/segment/frame/name/offset/type-index values agree.
The original packs them into two same-CODE records; native JWasm uses one.
Both complete raw packet lists and the explicit false packing-equality result
remain in the receipts. Original compiler identity, textual source order and
complete original OMF-program identity are not claimed.

## ABI and retained behavior

The divide and overflow interrupt entries retain their original full register
frames and IRET return, including DS setup and distinct handler reason codes.
The break entry retains PUSH SP, its original flags handling, duplicate POP BX,
saved vector restoration and RETF path. These instructions are preserved,
not replaced with a conventionalized interrupt wrapper.

The two public APIs remain far cdecl, preserving SI/DI/BP, six-byte local frames,
near-call-plus-PUSH-CS use of the private far-returning index helper and the
original six-signal mapping. One-time callback registration, DOS getvect/setvect
calls, previous-handler return, handler reset before dispatch, default/ignored
handler behavior, abort/exit paths and errno/result values remain unchanged.
The 38 initialized bytes retain both setup flags, six far handler slots and
the original lookup/reason bytes. No defensive handler validation is added.
Complete native comparison resolves this scope without an emulator matrix.

## Rejected and corrected native candidates

af546a retains the baseline listing. Eight accumulator CMP statements selected
different same-length encodings under JWasm, producing 22 byte differences;
explicit WORD immediates restore the original accumulator forms.

af546b restored all bytes and all 55 ordered fields, but its DATA/BSS GROUP
order differed from the original and actual parent member. The full scope
review rejected it; its raw source/OBJ/listing, native writer log and failure
comparison remain. af546c explicitly declares BSS/DATA and passes the complete
member review, including both ordered PUBLIC entries. Failed evidence is not
rewritten as acceptance.

## Affected native product proof

Parent after545 root SHA-256 is
`74e57df4ccf9f5b92225d7c0c3c8b56b413ca0c298f35056986a2179424d68ca`.
Only signal is assembled. Native TLIB preserves all 893 ordered member slots
and 892 other member programs. Source C0, unchanged game objects and the
validated actual OP cold pair are reused.

Two rounds each retain six complete raw outputs: signal OBJ, LIB, MAINL
EXE/MAP and OP EXE/MAP. All six repeat byte-for-byte. Nine successful native
phases/logs remain. The independent reviewer passed, checking source/profile/tool
bindings, actual native argv, independently reconstructed C0/library responses
and selected initialized/uninitialized material ownership.

| Output | Result |
| --- | --- |
| MAINL EXE | 67,372 bytes; complete original equality; 677 ordered MZ entries |
| OP EXE | 63,866 bytes; complete original equality; 607 ordered MZ entries |
| MAINL MAP | 80,967 bytes; complete after545 equality |
| OP MAP | 68,078 bytes; complete after545 and historical cold MAP equality |

Earlier actual packed OP proof is reused through unchanged decoded bytes and
tool identities. There is no new DIET run. The selected OP diagnostic now has
72 literal-equal streams and four order-only gaps: xxv, setvbuf, xalloc and xmsg.
C0's 58-field order, formal MAINL 0/250 acceptance and the unknown whole-game
denominator remain open. Diagnostic counts are not game progress credit.

Root: `.analysis/work/runtime-after546-build.json`, SHA-256 `8870088a19f3733dbd91f3b3fdc43c102155df7d257215cccad3dc5c3c24ff58`.
Producer/reviewer: `scripts/build_th03_runtime_after546_work.py` and
`scripts/review_th03_runtime_after546_work.py`; recipe:
`config/th03_runtime_after546.json`.

All twelve raw outputs/nine logs use `runtime-after546-*`. Independent review
transcript: `runtime-after546-independent-review.txt`. Actual source/profile/
config/driver and MAINL responses remain in `TH03ML/probe/af546d`; OP's consumed
C0/library/responses/outputs remain in `TH03OP/probe/af546d`. All af546a–c probes
and recipe scripts remain in `.analysis/work/probe/signal546/manifest.json`
(23 files, SHA-256 `e6d8845384879302b0e34afc5c9c1d479e40f3d10c93a6b7c2240763fd7cbc53`).
Displays were empty, writers serialized, one CPU at nice10. No full CI,
cold replay, game-object compilation, ancestor runtime replay or cleanup ran.
