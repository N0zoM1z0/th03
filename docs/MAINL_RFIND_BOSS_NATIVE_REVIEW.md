# Complete original C++ `rfind`: 3 full APIs, 971 CODE, 37 literal FIXUPPs

The original Japanese CL.LIB member **425** (`rfind`) has been reconstructed
as `src/mainl/crt/rfind.asm`. Unlike a partial search wrapper, the entire
native 971-byte C++ member is accounted for: **63 bytes `_TEXT` CODE**, **908
bytes `_TEXTC` CODE**, all three original far methods, complete original
exception metadata and typed string RTTI, zero DATA/BSS and 13 original
imports. Every executable opcode is native 8086 source, not machine-code
arrays or an object-file patch.

| Original `_TEXTC` offset | Far C++ public | Reconstructed implementation |
| ---: | --- | --- |
| 0 | `string::rfind(string &, unsigned)` | reverse-find front end, dispatches to original index helper |
| 71 | `string::rfind_index(const char *, unsigned, unsigned&)` | pattern preparation, reference management and reverse search |
| 282 | `string::rfind_case_index(const char *, unsigned, unsigned&)` | complete reverse case-insensitive path, long-index arithmetic and far matcher calls |

The `_TEXT` CODE region starts with the original five-byte exception-unwind
thunk, followed by the 10-byte cleanup frame at +5, three genuine 10-byte
catch descriptors at +15,+25,+35, and a compiler exception-state record
at +45..62. Far and near relocatable pointers target the *real interior
state fields* at `_TEXT+9` and +49, not the enclosing metadata bases. The
`_TEXTC` segment ends with the full original string RTTI at +850..907.

Native Borland emits the `_TEXT` FIXUPP fields in descending original offset
order `[61,35,25,15,9]` and the single `_TEXTC` LEDATA run's 32 fields in
descending order. TASM source declaration order was rebuilt using real
instruction and typed-data boundaries with symbolic `ORG`, matching **all
37 original FIXUPP fields literally, including their site, frame, target,
addend and ordering**. The original executable CODE segments also match
byte-for-byte. The complete Borland OMF record program still differs from
the new assembler's non-semantic metadata, so whole OBJ-record equality is
not claimed.

`scripts/build_th03_mainl_after353_work.py string-reverse-find-boss`
revalidates the entire previous **403-source** carrier, including the two
specifically documented `doslock` near-import TARGET/CODE frame differences.
It uses the parent helper to enforce *exactly these two* frame exceptions;
all other original fields remain uncompromised. Two native TASM/TLIB/TLINK
rounds reconstruct the original **893-member CRT library**, with **404
complete source-backed members**, **489 untouched original contextual
programs** and **130,205 original-equal logical CRT CODE bytes** (gain
**971**). Both rounds reproduce the entire original decoded Japanese
**67,372-byte MAINL EXE and MAP byte-for-byte**, including all **677
ordered DOS MZ relocations**.

The complete original/member and both native source-produced OBJ/LIB/EXE/MAP
sets, logs and source/parent/driver SHA receipts are retained under
`.analysis/work/after353-*`. The scoped reviewer and independent original
OMF/MZ checks are in `scripts/review_th03_mainl_after353_work.py` and
`tests/test_mainl_after353_work.py`. No full native cold replay, new formal
Factory accepted extent, canonical packed-unit credit or whole-game
source-ownership claim is implied.
