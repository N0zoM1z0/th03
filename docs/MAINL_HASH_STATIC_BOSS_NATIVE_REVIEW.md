# Original static TCharMask and string hashing: CODE, BSS, INIT and RTTI

The original Japanese Borland CL.LIB member **406** (`hash`) has been
reconstructed as complete original native 8086 source in
`src/mainl/crt/hash.asm`. This is the actual constructor and both string
hash algorithms, not a stub or a target-CODE blob:

| `_TEXTC` original offset | Complete original far C++ public |
| ---: | --- |
| 0 | `@TCharMask@$bctr$qv`, initialize a four-byte hash mask |
| 96 | `@string@hash$xqv`, case-sensitive/insensitive string hash dispatcher |
| 207 | `@string@hash_case$xqv`, original case-normalized hash calculation |

The original program has **50 bytes** of `_TEXT` CODE (five-byte unwind
thunk, native exception-state record and a true far static initialization
helper), **371 bytes** of `_TEXTC` CODE (three whole methods and the original
58-byte string RTTI at +313), genuinely uninitialized **four-byte `_BSS`**,
empty `_DATA`, and a real **six-byte `_INIT_`** record containing priority
`2001h` and a symbolic far call to `_TEXT+33`. Original DGROUP order
`0cff02ff03` and the imported string case-sensitivity switch are exact.

All **421 original CODE bytes**, three public offsets and symbol names,
seven original imported symbols, segment geometries, BSS/INIT sizes, **17
original relocation fields including source and target segments, frames,
addends and literal original FIXUPP order** match the pinned Japanese
CL.LIB member. Original Borland CODE-resident exception frames and string
RTTI are represented as typed `dw`/`dd` structures with real symbolic
addresses, not data misclassified as machine instructions. The source also
uses `ORG` at real instruction/metadata boundaries to emit the original
compiler's reverse-ordered local FIXUPP chronology. No binary or OBJ patch,
synthetic padding CODE, or alternative standalone vendor OMF was substituted.

`scripts/build_th03_mainl_after356_work.py string-hash-static-boss`
consumes all previous **407 source-backed CRT members** and rebuilds this
one entire object, the original **893-slot CRT library** and the exact
Japanese MAINL linker product in **two independent native TASM/TLIB/TLINK
rounds**. Both match the decoded Japanese **67,372-byte EXE and MAP**, with
all **677 DOS MZ relocations in the exact original order**. Working source
now covers **408 complete CRT members**, leaving **485 unchanged original
contextual programs**, and **131,776 original-equal logical CODE bytes**,
an increase of **421**. The complete raw native OBJ/LIB/EXE/MAP writer
rounds, logs and source/parent hashes are retained under
`.analysis/work/after356-*`; direct regression and reviewer are
`tests/test_mainl_after356_work.py` and
`scripts/review_th03_mainl_after356_work.py`.

Literal original ordered FIXUPPs and linked EXE/MAP are exact, but full
Borland OBJ metadata/record serialization remains different from TASM.
No full cold replay, new Factory-accepted extent, canonical packed-file
credit or whole-game source ownership is implied.
