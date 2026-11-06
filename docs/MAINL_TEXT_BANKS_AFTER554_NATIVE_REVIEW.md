# MAINL registration and ending DATA — after554

Two maintained semantic ASM TUs replace generated-only DATA context:
`src/mainl/data/registration.asm` and `src/mainl/data/ending_text.asm`.
The first uses the local `src/mainl/hiscore/regi_codes.inc` sprite alphabet.
Japanese text remains readable UTF-8 in source. Native staging performs only
strict, reversible UTF-8→CP932 and LF→CRLF conversion; no native bytes, names,
instructions or object records are rewritten.

## Complete bounded result

| Bank | Original address | Initialized bytes | Strings | PUBLIC entries | Ordered fields |
| --- | --- | ---: | ---: | ---: | ---: |
| Registration state/text | 0E3F:092E | 303 | 20 | 35 | 2 |
| Ending/verdict/staff text | 0E3F:0B3E | 360 | 41 | 82 | 0 |

Registration owns the nine eight-byte REGI sprite names, two near filename
pointers, four zero WORD input-hold counters, ten registration display names and
ten resource filenames. `rank_image_fn` retains its mutable `rft0.cdg` storage;
the existing consumer changes its fourth character by rank. `SCOREDAT_FN_PTR`
still points to `YUME.NEM`. Near-pointer sites72/74 retain the entire original
literal field stream: offset location1, width2, segment-relative=true, DGROUP
frame method1/index1, local-segment target method0/index2, addends214/223. No MZ
relocation is attached to these offsets.

The ending bank contains both ending script names, `op`, nine character names,
four fullwidth difficulty names, ten fullwidth digits, the score unit `点`, staff
music/palette filenames and twelve staff CDG filenames in original order.
All61 strings are bounded by their actual PUBLIC addresses and terminating NUL;
trailing/fullwidth spaces and CP932 spelling remain exact. All117 public
definitions and complete PUBLIC packet sets match the retained context.

Each native object has only empty CODE and WORD-aligned initialized DATA in
DGROUP. Every initialized byte is emitted once, including the registration
LIDATA expansion for the eight zero state bytes. No BSS, instruction arrays,
target-address constants or object patches are introduced.

## Honest object and alignment limits

The retained registration context explicitly wrote an extra final zero after
`over.m\0`, yielding304 DATA bytes. The maintained TU emits only its303 semantic
bytes. The following original `staffdat.cpp` contribution remains WORD-aligned
at0E3F:0A5E, so the normal current TLINK supplies one zero at**0E3F:0A5D**.
The source object has no initializer there. This proves the current linker
placement, not the original game's source intent; the byte remains unowned.
The two exact non-comment OMF differences are the DATA SEGDEF304→303 and omission
of that final LEDATA zero. All other original non-comment records, including
the complete ordered PUBLIC packets, remain equal.

Ending's original non-comment records apart from PUBLIC order remain equal.
Both sides contain82 single-definition PUBLIC packets with identical complete
contents, but eight digit-alias packets have a different emitted order. This
difference is retained explicitly. Both new complete raw objects repeat; no
original-game standalone OBJ or original assembler identity is claimed.

## Actual native production

Two direct pinned TASM5.0 assembly/TLINK6.10 rounds each produce both objects,
EXE and MAP. **All eight fresh raw outputs repeat**. The actual after553 C
picture table, after552 root TU, after548 source C0/library and32 cold project
objects are reused, with their complete consumed bytes/hashes checked. No TLIB,
packing, cold replay or ancestor runtime suite is run. Six actual writer logs
and all inputs/responses remain in `TH03ML/probe/af554b` and
`.analysis/work/text-banks-after554-native-*`.

| Native output per round | Bytes | SHA-256 |
| --- | ---: | --- |
| Registration OBJ | 1,352 | `7a5a804198ed2946f64269a8c3a8f601c43abf7bae710a8bfa989e1550958890` |
| Ending OBJ | 2,277 | `45f008c9c92859ac981454c99490eb3cc970f36dc69ebff49681cf04b7ba6e1d` |
| Complete decoded EXE | 67,372 | `92600c8858bb407516cac6a9d77538ebdf0c33522c4f6bd9194d569eb927134a` |
| Complete MAP | 81,039 | `fb5d7e3311c851416e673ea8dcbfff74f7e45d3e475042a2065ece3d9f3959d5` |

The entire decoded EXE and all677 literal ordered MZ relocations equal the
pinned Japanese target. Both bank MZ scopes are empty. The only MAP change
from after553 is registration's DATA contribution extent0130→012F; every other
raw MAP byte remains equal. Japanese provenance is `candidate-local-attested`;
independent pristine-dump identity is unknown.

Build receipt `.analysis/work/text-banks-after554-native-build.json`, SHA-256
`e498f16501b5b4d1c0f56a73fb65e4c87af607502da12b21730fd1a6eedafd89`.
Review receipt `.analysis/work/text-banks-after554-native-review.json`, SHA-256
`d7a8583e90631b29b009046b6fae68c9469bd9560e6525c3026c36540a90c642`.
Producer/reviewer: `build_th03_mainl_text_banks_work.py` /
`review_th03_mainl_text_banks_work.py`.

The initial DOS-bridge `tasm` invocation failed before producing an object.
TASM is installed as a separate native Win32 TASM32 executable; the successful
recipe uses that pinned path directly. Keep the failed af554a source/driver/
config snapshots, its report and writer/CLI logs. The18-file private manifest
at `probe/text554/manifest.json` also protects the previous218-owner publication,
ledgers and ownership audit. No tools, targets or native evidence were deleted.

## Publication and continuation

Two disjoint DATA owners add**663 bytes**, zero CODE, procedures or BSS.
MAINL reaches **220 extents / 290 procedures / 37,968 bytes**:34,431 CODE,
3,531 initialized DATA and six existing file-backed uninitialized bytes.
Authored ownership is17,717 bytes; library ownership remains20,251. The historical
registration trailing zero remains outside publication. Remaining project CODE
is still716 allocation bytes across9 contributions. These scopes are not a
whole-game denominator; canonical Factory acceptance remains0/250.

Future MAINL links retain both actual after554 objects plus the after553
picture table, after552 root and actual after548 C0/library references in the
new report's `rounds[i].reused`. Historical source/composer recipes stay frozen.

Affected checks pass: the scoped native review/publication, seven existing
acceptance-gate/SVG tests, `validate_tracking.py`, ownership audit `--check`,
progress `--check` and `git diff --check`. All218 prior ownership records are
unchanged; only the two disjoint DATA extents are added. The separate expensive
live-audit test is covered by publication and is not repeated. No full CI or
new emulator/input-matrix tests are needed for this DATA-only change.
