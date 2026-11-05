# Original string::copy — 737 CODE, seven RTTI descriptors, exact native link

The pinned Japanese Borland CL.LIB member **388** (`copy3`) now has complete
symbolic 8086 source at `src/mainl/crt/copy3.asm`. It implements the
original far `@string@copy$xqv` method: reference-counted copying,
allocation and `TStringRef` construction, with all original error and
exception-cleanup paths; it is neither an API stub nor a binary CODE array.

The `_TEXT` segment has **140 CODE bytes** with the real original far-unwind
thunk, typed exception state and reference-release cleanup helper. The
`_TEXTC` segment has **597 CODE bytes** with the complete 259-byte C++ method
and seven original typed RTTI descriptors (`TStringRef *`, `string *`, `xalloc`,
`xmsg`, `string`, `TStringRef`, `TReference`). DATA and BSS are empty.

All **737 original CODE bytes**, ten original imported symbols, public and
segment/DGROUP ABI (`0aff02ff03`), and **27 original literal ordered FIXUPP
fields** are reproduced by the native source, including the actual target,
frame, width, site and addend. Of these, nine are in `_TEXT` and 18 in
`_TEXTC`. Actual 8086 and typed RTTI declarations use `ORG` at original
boundaries to match the Borland relocation record sequence without dummy
machine-code arrays or post-link binary changes. Complete original Borland
OBJ record serialization still differs in unrelated metadata; full individual
OBJ-program identity is not claimed.

`scripts/build_th03_mainl_after380_work.py string-reference-copy-boss`
consumes the verified **476-member** source/receipt chain, recompiles this
entire member and reconstructs the original **893-slot CRT library**, then
runs two independent native TASM/TLIB/TLINK rounds. Both reproduce the
original decoded Japanese **67,372-byte MAINL EXE and MAP byte-for-byte**,
including all **677 ordered DOS MZ relocations**. Working CRT source now
covers **477 complete source-backed original-equal members**, leaving **416
unchanged contextual programs**, with **152,556 source-built original-equal
CODE bytes** (+737). Original and source-built OBJ/LIB/EXE/MAP pairs, tool
logs, driver/source/parent hashes, reviewer and OMF/MZ tests are retained
under `.analysis/work/after380-*`,
`scripts/review_th03_mainl_after380_work.py` and
`tests/test_mainl_after380_work.py`.

This is scoped working-source evidence, not new formal Factory acceptance,
canonical packed-file credit or proof of whole-game source completeness.
No full cold replay was run.
