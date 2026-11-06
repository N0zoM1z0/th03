# Shared DOS environment and stdio after544

Two existing runtime members, dosenv and write, now reproduce all 723 CODE
bytes and 14 literal ordered relocation fields. setvbuf preserves its complete
289 CODE/4 initialized DATA bytes and all per-site attributes, but two MOV
operand-fixup pairs remain unordered. It is explicitly not ordered-exact.
These are refinements of existing owners, with zero new member, CODE-extent
or authored-function credit and no whole-product source acceptance.

## Complete original scopes

The original is the independently opened installed TC4 CL.LIB, SHA-256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
Japanese product targets retain `candidate-local-attested` provenance;
independent pristine-dump attestation remains unknown. Reconstructed carriers
do not supply the original.

| Member / slot | Live owner in src/shared/crt | CODE | DATA | BSS | Ordered fields |
| --- | --- | ---: | ---: | ---: | --- |
| dosenv / 25 | dos_environment.asm | 365 | 0 | 0 | All five equal |
| write / 331 | write_stream.asm | 358 | 0 | 0 | All nine equal |
| setvbuf / 285 | stdio_buffer.asm | 289 | 4 | 0 | Two operand pairs still open |

All original segment widths, attributes, GROUP/ALIAS/MODEND, import order,
public ownership, ordered PUBLIC entries and raw PUBLIC packet lists agree.
All initialized bytes are written exactly once; there are no holes or overlaps.
All three use the pinned compatible JWasm profile and unchanged bounded
`src/mainl/crt/stdio_layout.inc`. Historical dosenv/setvbuf and after538
dos_write TUs remain unchanged ancestor inputs. Original compiler identity and
complete original OMF-program identity are not claimed.

dosenv's five original/native sites are `319,220,130,100,51`.
write's nine are `315,230,115,98,80,66,49,23,14`. Complete field geometry,
segment-relative flag, frame, target method/index and addend agree directly
in emitted order. In particular, write's near IOERROR at CODE23 keeps TARGET
frame5 from after538; a default segment frame would be wrong.

## ABI and behavior

DOSENV retains its near RET12 callee cleanup, three far arguments and ten-byte
local frame. It counts and copies the caller environment, stops on a null or
empty entry, retains optional executable-name suffix construction and returns
the raw allocation through the caller output pointer. Its aligned working
cursor uses offset-only arithmetic; word overflow and the existing unsigned
8000h bound remain as in the original. Explicit WORD immediate forms retain
the original accumulator ADD encodings.

write retains its far C ABI, SI/DI preservation and 144-byte translation scratch.
Descriptor validation, zero/FFFFh count behavior, append seek, binary direct
write, text LF-to-CRLF conversion, 128-byte flush threshold and original short
write accounting remain unchanged. No pointer normalization or defensive
validation is introduced. Complete native equality resolves these scopes
without an emulator or input-domain matrix.

setvbuf retains token/mode/size validation, the two initialized standard-stream
flags, fseek/free behavior, default hold pointer, allocation/ownership flags,
buffer installation and line buffering. Its two symbolic callback MOVs remain
real instructions. They each have a destination fixup and an immediate fixup:

| Stream | Complete CODE sites, in emitted order |
| --- | --- |
| Original | 210,196,194,190,188,129,103,77,71,63,55,49,41 |
| Native | 210,194,196,188,190,129,103,77,71,63,55,49,41 |

The unresolved pairs are `(196,194)` and `(190,188)`. Every complete per-site
attribute agrees, but their sequence does not. Both lists and the explicit
false equality result remain in config, producer and independent reviewer.
No sorting, byte arrays, padding or output patches manufacture equality.
Bounded ordinary source spans restore the other field chronology, while
prebound private branch labels retain exact displacements and one-write coverage.

## Native producer investigation

af544a–n retain source, OBJ/listing outputs where produced, recipes, logs and
scope reports. The tested BCC45 naked/global declarations were rejected; the
accepted global-asm form emitted DATA without a public CODE body. NASM emitted
the same ascending operand-pair order. Plain C ABI probes emitted 16 rather
than the required 20-byte abort body; no dummy register uses or manual byte
encoding were adopted. af544c/d are identical source probes, not distinct
recovery evidence.

An isolated Turbo C++ 1.01 candidate was obtained from the official museum
archive at `https://altd.embarcadero.com/download/museum/tcpp101.zip`.
Archive SHA-256 is
`9f8c8df36c7faa0d32cca1a871761de3fcab9a8b769bab93a414e14c403f92fc`;
the extracted TCC.EXE is
`74cedc2863e9ba7776917b713cb2956b38d982731bebbd008468d203ba07d272`.
It resides privately under TC101, without replacing TC4 or production tools.
Preflight passed after installation. Its register-flag variants still emitted
the 16-byte ABI probe; inline ASM delegated to external TASM and failed to find
that executable. This candidate is neither a production dependency nor proof
of original compiler identity. It does not close the setvbuf question.

The 110-file diagnostic manifest is
`.analysis/work/probe/environment-stdio544/manifest.json`, SHA-256
`51f8df7bc95cb9c13019383f6d933350b25559c2a14292abc5cf576af442033a`.
It retains the temporary recipe scripts, both environment-change preflights,
download/install provenance and tool bytes. Diagnostic counts add no source
acceptance credit.

## Affected native product proof

Parent after543 root SHA-256 is
`b214dc7f1af9d38e6bc15d90bb673cd864a508d78b64246c502c85c8ca5a108d`.
Only the three listed owners are assembled. Native TLIB retains all 893
ordered slots and 890 other member programs unchanged. Source C0, unchanged
game objects and the validated actual OP cold pair are reused.

Two rounds each preserve eight complete raw outputs: three OBJ files, LIB,
MAINL EXE/MAP and OP EXE/MAP. All eight repeat byte-for-byte. Thirteen successful
native phases/logs remain. The independent reviewer passed, checking actual
consumed source/include/profile/tool bindings, native argv, independently
reconstructed C0/library responses and selected material ownership.

| Output | Result |
| --- | --- |
| MAINL EXE | 67,372 bytes; complete original equality; 677 ordered MZ entries |
| OP EXE | 63,866 bytes; complete original equality; 607 ordered MZ entries |
| MAINL MAP | 80,967 bytes; complete after543 equality |
| OP MAP | 68,078 bytes; complete after543 and historical cold MAP equality |

Earlier actual packed OP proofs are reused through unchanged decoded bytes and
tool identities; there is no new DIET run. The selected OP diagnostic now has
69 literal-equal streams and seven order-only gaps: xxv, fbrk, signal, setvbuf,
xalloc, xmsg and loadprog. C0's 58-field order, formal MAINL 0/250 acceptance
and the whole-game denominator remain open. These counts are not game progress.

Root: `.analysis/work/runtime-after544-build.json`, SHA-256
`5382d231ccf9cc1ae3f59b365524277b5e983ba7d5f2dba2b82f21ff7c3cd087`.
Producer/reviewer: `scripts/build_th03_runtime_after544_work.py` and
`scripts/review_th03_runtime_after544_work.py`; recipe:
`config/th03_runtime_after544.json`.

All sixteen raw outputs/thirteen logs use `runtime-after544-*`. Independent
review transcript: `runtime-after544-independent-review.txt`. Actual source,
include/profile/config/driver and MAINL responses remain in `TH03ML/probe/af544o`;
OP's consumed C0/library/responses/outputs remain in `TH03OP/probe/af544o`.
Displays were empty, writers serialized, one CPU at nice10. No full CI, cold
replay, game-object recompilation, ancestor runtime replay or cleanup occurred.
