# Full original Borland string::assign: 791 CODE, typed RTTI and exception ABI

The original Japanese CL.LIB **member 381** (`assign`) is reconstructed as
real 8086 symbolic instructions and compiler-typed `dw`/`dd` metadata in
`src/mainl/crt/assign.asm`. The member contains the **complete 665-byte
string::assign far C++ method**, and the preceding **126-byte `_TEXT`** segment:
its true unwind thunk, typed exception state and complete far reference-
destructor cleanup helper. The method itself includes original argument
bounds, reference counting, allocation and exception paths, not just an API
wrapper. The original `_DATA` and `_BSS` are empty.

The second CODE segment includes five complete Borland C++ RTTI structures
at +404 (`TStringRef *`), +427 (`xalloc`), +493 (`xmsg`), +549 (`TStringRef`)
and +619 (`TReference`). All original public/interface names and offsets,
**8 imported Borland symbols**, original group `0aff02ff03`, and all **791
CODE bytes** match the pinned Japanese original member. The **24 complete
original FIXUPPs** match literally in physical record order, frame, width,
target and addend: 7 in `_TEXT` and 17 in `_TEXTC`, descending within each
original BCC LEDATA run. The source uses `ORG` only for genuine 8086 and
typed RTTI/source field boundaries; no embedded executable CODE array,
dummy filler or binary OBJ/EXE patch is used. Full original Borland OMF
record serialization remains different in ancillary metadata and is not
claimed byte-identical.

`scripts/build_th03_mainl_after369_work.py string-assign-boss` inherits the
**444-source** original Japanese CRT receipt chain, reconstructs this member
and the complete original **893-slot** library, then performs **two actual
native TASM/TLIB/TLINK rounds**. Both reproduce the original decoded
**67,372-byte Japanese MAINL EXE and complete MAP byte-for-byte**, including
all **677 ordered DOS MZ relocations**. The verified working source reaches
**445 complete CRT members**, **448 unchanged contextual original programs**
and **141,719 source-compiled original-equal CODE bytes**, an increase of
**791**. Raw original/TASM OBJ/LIB/EXE/MAP, writer logs and source/parent
SHA receipts are retained under `.analysis/work/after369-*`. The scoped
reviewer and direct OMF/MZ regression checks live in
`scripts/review_th03_mainl_after369_work.py` and
`tests/test_mainl_after369_work.py`.

No full cold replay, new Factory-accepted decoded extent or canonical
packed-product credit is inferred from this working-source proof.
