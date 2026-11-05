# Complete original C-string range constructor: 811 CODE and six RTTI types

The original pinned Japanese CL.LIB member **392**, `ctor4`, now has full
natural 8086 source in `src/mainl/crt/ctor4.asm`. The exported Borland far
C++ constructor `@string@$bctr$qnxcuiui` handles C-string range bounds,
reference-counted buffer construction, capacity allocation and all original
exception/unwind and destruction paths, not just an API forwarding stub.

The original `_TEXT` segment holds **207 CODE bytes** (compiler exception
metadata and complete far cleanup helpers); `_TEXTC` holds **604 CODE bytes**
(the full constructor and six typed C++ RTTI structures: `TStringRef *`,
`string::lengtherror`, `xalloc`, `xmsg`, `TStringRef`, `TReference`). DATA and
BSS are empty. All **811 original CODE bytes**, nine actual imported symbols,
public name/offset, segment geometry and group `0aff02ff03` match the
pinned original Japanese OMF member.

The source-built OBJ reproduces all **29 original FIXUPP fields literally in
record order**, including 11 compiler exception and 18 method/RTTI fields,
frames, targets and addends. This uses real instructions and typed `dw`/`dd`
declarations at their actual Borland `ORG` offsets; no executable bytes were
embedded as data and no OBJ/EXE/MAP bytes were patched. Complete original
Borland OMF member *serialization* still differs in ancillary records, so
full OBJ-program equality is **not** claimed.

`scripts/build_th03_mainl_after379_work.py string-cstr-range-constructor-boss`
revalidates the **475-member** source/receipt-bound parent, replaces only
`ctor4`, and rebuilds all original **893 CRT library slots** under two actual
native TASM/TLIB/TLINK rounds. Both reconstruct the exact original decoded
Japanese **67,372-byte MAINL EXE and MAP**, including all **677 ordered MZ
relocations**. Working-source coverage becomes **476 complete members**, **417
unchanged contextual original programs**, and **151,819 original-equal source
CODE bytes** (+811). The raw source/native OBJ/LIB/EXE/MAP vectors, logs,
source and parent SHA receipts, review and original-member tests are retained
under `.analysis/work/after379-*`, `scripts/review_th03_mainl_after379_work.py`
and `tests/test_mainl_after379_work.py`.

This is original CODE and linked-working-source evidence, not new formal
Factory acceptance or a full packed-game source ownership claim. No full
cold replay was run.
