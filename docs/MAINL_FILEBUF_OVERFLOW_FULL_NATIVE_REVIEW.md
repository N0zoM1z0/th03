# Complete original filebuf::overflow: buffer flush, put/get-area maintenance

The original Japanese Borland CL.LIB member **712** (`fsboflow`) is restored
as full symbolic native 8086 source in `src/mainl/crt/fsboflow.asm`.
`@filebuf@overflow$qi` is a **333-byte** implementation, not a forwarding
leaf: it checks binary/text and output mode state, flushes pending bytes,
updates put/get-area pointers, performs original far virtual streambuf
calls, handles EOF and short writes, and writes a pending character or
signals the original overflow failure. Its original `_TEXTA` CODE, empty
`_DATA` and `_BSS`, group `08ff02ff03` and complete far ABI are preserved.

The original library contains exactly three imported far references:
`_write`, `@streambuf@setp$qnct1`, `@streambuf@setg$qnct1t1`. The
original BCC FIXUPP order is **CODE+244, +210, +82**. A forward TASM
source would emit the same machine CODE but invert these record locations;
the recovered source uses `ORG` at three actual original imported-call
instruction boundaries (+243, +209, +0) in descending order. That restores
the **three literal original FIXUPP fields, frames, targets and record
order** without patched binary outputs or machine-code data arrays.
The full original Borland OBJ program metadata differs from TASM's
serialization, so full OBJ program-record identity is not claimed.

`scripts/build_th03_mainl_after359_work.py filebuf-overflow-boss` validates
the parent **411-member** source/receipt chain, reassembles only the changed
member and rebuilds the original 893-position Borland CRT library in **two
independent native TASM/TLIB/TLINK rounds**. Both rounds reproduce the
**67,372-byte decoded Japanese MAINL EXE and full MAP** byte-for-byte,
including the entire **677-item ordered MZ relocation inventory**. The
working CRT now has **412 complete original-equal source members**, **481
unchanged original contextual members**, and **133,078 source-built
original-equal logical CODE bytes**, an increase of **333**. The original
CL.LIB OMF and raw source-produced OBJ/LIB/EXE/MAP, writer logs and SHA
receipts are retained under `.analysis/work/after359-*`, with tests in
`tests.test_mainl_after359_work` and scope review in
`scripts/review_th03_mainl_after359_work.py`.

This is source-bound working CRT verification, not new Factory-accepted
canonical decoded extent, packed-unit credit or whole-game exactness.
No full cold replay was run.
