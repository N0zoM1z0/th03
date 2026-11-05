# Full original Borland C++ diagnostic runtime (`checks`): 89 relocations

This increment reconstructs the **actual original Japanese CL.LIB member
382** as `src/mainl/crt/checks.asm`: **1,708 complete CODE bytes** in two
segments (`_TEXT` 221, `_TEXTC` 1,487), **143 initialized DATA bytes**, an
empty BSS, and true six-byte `_INIT_` and `_EXIT_` records. All **seven
exported far C++ methods** and **three original DATA publics**, **18 imported
Borland symbols**, all original segment sizes and group `0eff02ff03` are
retained. The recovered implementation includes `TDiagGroupDef::Trace/Warn`,
`TDiagBase::Output/Message/Trace/Warn`, `xerror::MakeString`, native
`ostrstream` formatting, static construction/destruction, unwind state and
eight complete C++ RTTI records (`string *`, `ostrstream`, `ios`, `ostream`,
`strstreambase`, `string`, `strstreambuf`, `streambuf`).

The original DATA includes the real initialized group-name pointer, flags,
**98 materialized zero-valued bytes** of `@TDiagBase@Out`, and eight distinct
original message fragments (`Def`, `: [`, `] `, CR/LF, `Trace`, `Warning`,
` failed `, `: `). During actual source reconstruction, a TASM `DUP(0)`
declaration was found to emit an **uninitialized LEDATA hole**, not the
original 98 initialized bytes. Explicit zero initializers repair the actual
source semantics, not a postassembly binary patch. The CODE segments
contain real 8086 instruction mnemonics, while exception records and RTTI
are genuine symbolic `dw`/`dd` and ASCII declarations, not opaque executable
machine-code arrays.

All **89 original relocation fields** match the actual original Japanese
CL.LIB in site, segment, width, target method and identity, frame and
addend. The revised native source now also matches **all 89 original
FIXUPP records in literal sequence**, including both original CODE
segments, DATA, INIT and EXIT fields. The first forward-source build
already reproduced the complete linked EXE/MAP but reordered some OMF
relocations; placing genuine 8086 and typed-data declarations at their
original boundaries in descending BCC record order resolved this last
FIXUPP chronology issue without changing a single CODE or DATA byte.
The complete Borland OMF program serialization **still differs** in other
nonsemantic COMENT/LEDATA/PUBDEF records; full OBJ identity is not claimed.

`scripts/build_th03_mainl_after361_work.py diagnostic-checks-boss`
consumes the parent **420-source** CRT carrier, recompiles this whole member
and rebuilds the original **893-slot** library in two independent native
TASM/TLIB/TLINK rounds, without running full cold replay. Both rounds
reproduce the **original decoded 67,372-byte Japanese MAINL EXE and MAP
byte-for-byte**, including **all 677 ordered DOS MZ relocations**. That
is stronger linked-output evidence than CODE byte equality alone; the
non-identical full Borland OBJ metadata remains independently visible.

The scoped working carrier now covers **421 complete source-backed members**,
**472 original contextual library programs**, and **135,508 original-equal
CRT CODE bytes** (+1,708), plus this member's real initialized DATA and
INIT/EXIT records. Raw original and source-produced OBJ/LIB/EXE/MAP files,
source/parent/driver hashes and writer logs are under
`.analysis/work/after361-*`; the independent reviewer and raw OMF/MZ tests
are `scripts/review_th03_mainl_after361_work.py` and
`tests/test_mainl_after361_work.py`.

This is **working-source evidence**, not a new Factory-accepted decoded
extent, packed-game file ownership or whole-game exactness claim.
