# Original C++ `string` substring-range constructor: full 716-byte boss

The pinned Japanese Borland CL.LIB **member 393** (`ctor5`) is now
reconstructed as complete native symbolic 8086 source in
`src/mainl/crt/ctor5.asm`. Its far C++ public
`@string@$bctr$qmx6stringuiui` performs the original substring/range
copy construction, allocation, `TStringRef` reference handling and all
exception cleanup paths; it is not an import stub or target-CODE byte array.

The original `_TEXT` holds **126 CODE bytes** including the real far unwind
thunk, typed exception state and complete far reference-release helper.
The `_TEXTC` holds **590 bytes**, the complete original 329-byte
constructor and five genuine typed RTTI records at +329 (`TStringRef *`),
+352 (`xalloc`), +418 (`xmsg`), +474 (`TStringRef`) and +544 (`TReference`).
DATA/BSS are empty.

All **716 original CODE bytes**, eight original Borland import names,
original public offset, segment/group layout `0aff02ff03`, and all **22
original OMF FIXUPP fields** are reproduced **literally in original
record order**, including seven exception-state and fifteen constructor/
RTTI fields. Frame, target, width, site and addend match the true original
Japanese CL.LIB. The source emits genuine 8086 and compiler typed `dw`/
`dd` statements at original offsets, not executable CODE arrays or patched
binary/OBJ/MAP files. The full original Borland OMF program serialization
still differs in ancillary metadata and is not claimed byte-identical.

`scripts/build_th03_mainl_after377_work.py string-substring-constructor-boss`
revalidates the **473-source** original Japanese CRT parent, compiles
this whole original member and reconstructs the **893-slot CL.LIB** and
full decoded Japanese MAINL link with native TASM/TLIB/TLINK in **two
independent rounds**. Both reproduce the original **67,372-byte EXE and
complete MAP byte-for-byte**, including all **677 ordered DOS MZ
relocations**. The working CRT reaches **474 complete original-equal
source-backed members**, **419 unchanged original contextual programs**
and **150,387 source-compiled original-equal CODE bytes** (+716).
Original/source native OBJ/LIB/EXE/MAP, full writer logs, source/parent
SHA receipt and independent regression checks remain under
`.analysis/work/after377-*`, `scripts/review_th03_mainl_after377_work.py`
and `tests/test_mainl_after377_work.py`.

This is working CRT source proof, not full cold replay, new formal Factory
source acceptance or canonical packed-image ownership.
