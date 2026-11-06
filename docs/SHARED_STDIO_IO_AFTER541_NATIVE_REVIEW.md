# Shared stdio IO and positioning after541

The existing fflush and fseek runtime members now reproduce all eight literal
ordered relocation fields and all 701 initialized CODE bytes. The fseek member
includes its private buffered-byte helper, fseek and ftell. This refines existing
owners; new member, CODE-extent and authored-function credit remain zero.

Live sources are `src/shared/crt/flush_stream.asm` and
`src/shared/crt/stream_position.asm`, with unchanged bounded
`src/mainl/crt/stdio_layout.inc`. Historical `src/mainl/crt/fflush.asm` and
`fseek.asm` remain unchanged ancestor inputs.

## Complete original scopes

Original installed TC4 CL.LIB is independently opened, SHA-256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
No reconstructed carrier supplies the original. Product targets remain pinned
Japanese `candidate-local-attested`; independent pristine-dump provenance is unknown.

| Member / original slot | CODE | DATA / BSS | Literal field sites, in order |
| --- | ---: | ---: | --- |
| fflush / 219 | 209 | 0 / 0 | +169, +17 |
| fseek / 232 | 492 | 0 / 0 | +409, +365, +342, +293, +239, +149 |

Seven fields are FAR calls with original TARGET frame method 5 and EXTDEF target
method 2. fseek's +342 is the 16-bit DGROUP-framed `__openfd + 1` reference,
frame method 1, target method 2, import index 3 and addend 1. All full field
attributes and import indices match directly in emitted order. Lists are never
sorted to claim ordered equality.

The review checks all initialized bytes and complete initialization coverage,
segment extents/attributes (28h/48h/48h), literal GROUP/ALIAS/MODEND, imports and
all public ownership. There are no CODE holes or extra exported helpers.

## Native emitters and PUBLIC records

fflush retains TASM. Its pending-output span 126–208 precedes its entry/input
span 0–125 in the emitted record stream, recovering the two original fields.

fseek uses the already pinned compatible JWasm profile. Its private near-Pascal
helper stays at 0–136 with RET 4. Ordinary source spans then emit restoration/
return 390–491, append query 347–389, append test 331–346, ftell entry 267–330,
fseek adjustment 164–266 and fseek entry 137–163. These cover every byte once;
there is no padding, target instruction array or object/output patch. Original
compiler textual statement order is not claimed.

Four `cmp ax,word ptr -1` operations retain the original accumulator-immediate
encoding at +251/+311/+383/+421. The first compatible-emitter trial used the
same-length sign-extended generic form, causing eight byte differences; it was
rejected. Explicit WORD immediates reproduce every original byte without adding
instructions. `buffered_bytes` is PRIVATE, so it adds no PUBLIC. The compatible
GROUP declaration preserves original DATA/BSS order through that emitter.

The original fseek PUBLIC stream is `_fseek` at 137 then `_ftell` at 267, both
group 0, CODE segment 1, type index 0. TASM trials emitted the reverse order
despite declaration/definition-order changes and were rejected. JWasm emits
both entries in the original order but packs them into one PUBDEF record;
the original has two records. The review directly compares every ordered PUBLIC
entry, including group, segment, frame, name, offset and type index. It retains
both raw packet lists and explicitly requires this packing difference. It does
not sort entries or claim literal packet equality. fflush's one PUBLIC packet
remains raw-equal. Data-record packing also differs; original OMF-program
identity is false for both members.

## ABI and original behavior

fflush retains the far FILE argument, BP-2 pending-count word and SI/DI frame.
A null FILE invokes flushall. Token validation, buffered-input/hold-pointer
handling and line-buffer flags retain the original comparisons and widths.
Pending output resets FILE level/current pointer before `___write`; short writes
mark F_ERR and fail except for the original terminal exception. No new checks
or error-policy changes were added.

fseek retains its far FILE, signed 32-bit offset and 16-bit origin arguments.
It flushes first, preserves relative buffered-byte adjustment, resets original
EOF/input/output state and calls lseek with the original long failure comparison.
ftell retains physical position, buffered count and text LF expansion. Append
output temporarily queries end position, restores the old position and preserves
both seek-failure paths before adding pending bytes. The helper retains backward
output and forward input scans, 16-bit arithmetic and near callee cleanup.
External FILE storage does not become private DATA/BSS ownership. Complete native
bytes resolve this scope without a new emulator model or input-domain matrix.

## Affected native product proof

Parent after540 root SHA-256 is
`568fed759f13881ea179eb3d874afaa49e1c1ae5b8022c78ebf5dbebf4bb776a`.
Only these two members are assembled. Native TLIB retains all 893 slots and
891 other member programs unchanged. Source C0 and unchanged current game
objects are reused; the actual OP cold pair and source graph are validated.

Each of two native rounds retains seven complete raw outputs: both OBJ files,
LIB, MAINL EXE/MAP and OP EXE/MAP. All seven repeat byte-for-byte. All eleven
successful writer phases/logs remain. Tools and compatible profile/source are
attested; native commands and consumed linker responses are independently checked.

| Output | Result |
| --- | --- |
| MAINL EXE | 67,372 bytes; complete original equality; 677 ordered MZ entries |
| OP EXE | 63,866 bytes; complete original equality; 607 ordered MZ entries |
| MAINL MAP | 80,967 bytes; complete after540 equality |
| OP MAP | 68,078 bytes; complete after540 and historical cold MAP equality |

All selected runtime material storage and MAP ownership are rechecked against
real original CL.LIB. Actual earlier packed OP proofs are reused through unchanged
decoded bytes and tool identities; no new DIET run is represented. The OP-selected
diagnostic now has 62 equal literal streams and 14 order-only gaps. C0's 58-field
ordering question, formal MAINL 0/250 acceptance and whole-game denominator remain
open; these diagnostics add no source/function acceptance.

Root: `.analysis/work/runtime-after541-build.json`, SHA-256
`1799436476f816e7b921ce29997343c2f08d64b5a3f73c5153d87c68117ecdce`.
Producer/reviewer: `scripts/build_th03_runtime_after541_work.py` and
`scripts/review_th03_runtime_after541_work.py`; recipe:
`config/th03_runtime_after541.json`.

All fourteen raw outputs and eleven logs use `runtime-after541-*`. The independent
review transcript is `runtime-after541-independent-review.txt`. Consumed sources,
include, profile, config, driver, extracted objects and MAINL responses remain in
`TH03ML/probe/af541f`; OP's consumed C0/library/responses and outputs remain in
`TH03OP/probe/af541f`. All af541a–e trials remain under
`.analysis/work/probe/stdio541/manifest.json` (40 pinned files). Displays were
empty, writers serialized, one CPU at nice10. No full CI, cold replay, game-object
recompilation, ancestor runtime chain or output cleanup occurred.
