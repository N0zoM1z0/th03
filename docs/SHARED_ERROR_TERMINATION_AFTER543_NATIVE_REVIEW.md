# Shared error conversion and termination after543

Three existing runtime members now reproduce all 24 literal ordered fields,
14 ordered PUBLIC entries, 301 CODE bytes and 105 initialized DATA bytes.
The 128-byte atexit callback table remains uninitialized BSS. This refines
existing owners and adds no member, storage extent or authored-function credit.

Live owners are `src/shared/crt/io_error.asm`, `atexit_register.asm` and
`process_exit.asm`, using the pinned compatible JWasm profile. The unchanged
bounded includes are `src/mainl/crt/crt_errno.inc` and `dos_error_map.inc`.
Historical ioerror_link/atexit/exit TUs remain unchanged ancestor inputs.

## Complete original scopes

The actual installed TC4 CL.LIB is independently opened, SHA-256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
A reconstructed carrier does not supply the original. Japanese product targets
retain pinned `candidate-local-attested` provenance; independent pristine-dump
attestation is unknown.

| Member / slot | CODE | DATA | BSS | Literal field sites, in order |
| --- | ---: | ---: | ---: | --- |
| ioerror / 79 | 82 | 91 | 0 | CODE22,28,45,39,51 |
| atexit / 5 | 49 | 2 | 128 | CODE41,37,33,19,7 |
| exit / 42 | 170 | 12 | 0 | CODE84,78,74,56,51,48,42,36,32,24,20; DATA8,4,0 |

All complete geometry, segment-relative status, frame, target method/index and
addend values match in emitted order, without sorting. Imports, segment widths,
attributes, GROUP/ALIAS/MODEND and public ownership also agree. ioerror retains
its original BSS/DATA GROUP order; the other two retain DATA/BSS.

Every initialized CODE/DATA byte is emitted once, without gaps or overlapping
records. The complete uninitialized-site vectors are checked: atexit BSS0–127
remains reserved, and all CODE/DATA extents are fully initialized. The original
callback DATA is three genuine symbolic FAR initializers to the private far
no-op procedure, not a raw twelve-byte target array.

## Ordered publication across CODE and DATA

The pinned native writer traverses its PUBLIC queue and starts a new PUBDEF
packet when its segment changes. Source now places declarations/definitions in
the actual original cross-segment order:

| Member | Original ordered entries |
| --- | --- |
| ioerror | CODE __IOERROR@0; DATA __dosErrorToSV@2, __doserrno@0; CODE __DOSERROR@62 |
| atexit | CODE _atexit@0; DATA __atexitcnt@0; BSS __atexittbl@0 |
| exit | CODE _exit@95, __exit@114; DATA __exitbuf@0, __exitfopen@4, __exitopen@8; CODE __cexit@136, __c_exit@154 |

All entry group/segment/frame/name/offset/type-index values are directly equal
in that order. Both complete raw packet lists remain in the receipts. atexit's
three packets are raw-equal. ioerror packs four original records into three;
exit packs seven into three. Those differences are explicitly required and
are not represented as raw packet equality. CODE/DATA record packing differs
too; complete original OMF-program identity remains false.

Ordinary bounded source spans preserve fixup chronology. No padding, instruction
byte arrays, output patches or extra helper exports are used. The empty far
callback remains a real five-byte callable body with original SI/DI preservation.
The private near engine has RET6 callee cleanup for its three word arguments;
the historical "caller-popped" comment is inaccurate and its frozen file is
not edited. Original compiler identity/textual source order is not claimed.

The first exit candidate matched fields/PUBLIC order but emitted FE instead of
E9 at CODE40, giving the wrong loop displacement. It was rejected and retained.
Defining the real backward-loop label at 18 before emitting the separately
ordered test span restores every original byte. af543b verifies the corrected
candidate; no object patch supplies the displacement.

## ABI, storage and behavior

ioerror retains its two near RET2 interfaces, signed DOS/System V selection,
DOS mapping limit/fallback, original errno words and the signed INT_MIN negation
case. DOSERROR still returns its original argument after calling IOERROR.

atexit retains its far callback argument, 32-entry table, initialized word count,
four-byte callback stride and original zero/one result. Capacity checking remains
equality with 32; no defensive greater-than check or callback validation is added.

exit retains LIFO callback traversal, cleanup/buffer callback, restore/checknull
calls, returning and quick variants, file/open callbacks and terminate path.
The four far public wrappers retain their actual arguments, return frames and
SI/DI/BP preservation. Dynamic callbacks remain writable DATA initialized to
the private FAR no-op body; reserved callback storage remains BSS. Complete
native equality resolves this scope without an emulator or input-domain matrix.

## Affected native product proof

Parent after542 root SHA-256 is
`fee3d18425d239420999d2c8771c28c10310df7225a50f927fbabb29ae8c8c08`.
Only these three members are assembled. Native TLIB retains all 893 ordered
slots and 890 other member programs unchanged. Source C0, unchanged game objects
and the validated actual OP cold pair are reused.

Two rounds each retain eight complete raw outputs: all three OBJ files, LIB,
MAINL EXE/MAP and OP EXE/MAP. All eight repeat byte-for-byte. Thirteen successful
native phases/logs remain. The independent reviewer verifies the actual source,
include/profile/tool bindings, native argv, reconstructed C0/library responses
and selected initialized/uninitialized material ownership.

| Output | Result |
| --- | --- |
| MAINL EXE | 67,372 bytes; complete original equality; 677 ordered MZ entries |
| OP EXE | 63,866 bytes; complete original equality; 607 ordered MZ entries |
| MAINL MAP | 80,967 bytes; complete after542 equality |
| OP MAP | 68,078 bytes; complete after542 and historical cold MAP equality |

The original earlier packed OP proofs are reused through unchanged decoded
bytes and tool identities; no new DIET run is represented. The OP-selected
diagnostic is now 67 literal-equal streams and nine order-only gaps. C0's
58-field order, formal MAINL 0/250 acceptance and whole-game denominator remain
open. No new source/function acceptance is inferred from diagnostic counts.

Root: `.analysis/work/runtime-after543-build.json`, SHA-256
`b214dc7f1af9d38e6bc15d90bb673cd864a508d78b64246c502c85c8ca5a108d`.
Producer/reviewer: `scripts/build_th03_runtime_after543_work.py` and
`scripts/review_th03_runtime_after543_work.py`; recipe:
`config/th03_runtime_after543.json`.

All sixteen raw outputs/thirteen logs use `runtime-after543-*`. Independent
review transcript: `runtime-after543-independent-review.txt`. Actual source,
includes/profile/config/driver and MAINL responses remain in `TH03ML/probe/af543c`;
OP's consumed C0/library/responses/outputs remain in `TH03OP/probe/af543c`.
All af543a/b candidates and scope/recipe proofs remain under
`.analysis/work/probe/error-termination543/manifest.json` (28 pinned files).
Displays were empty, writers serialized, one CPU at nice10. No full CI, cold
replay, game-object recompilation, ancestor runtime chain or cleanup occurred.
