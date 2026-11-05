# Original `string::reserve`: complete capacity-management and C++ exceptions

The Japanese Borland CL.LIB **member 423** (`reserve`) has been
reconstructed as true symbolic 8086 native source in
`src/mainl/crt/reserve.asm`. The complete C++ far function
`@string@reserve$qui` includes original reference-counted capacity
handling and delegation to `TStringRef::reserve`, with complete cleanup
paths and the real Borland allocation/error behavior — not merely a
forwarding stub.

Its original `_TEXT` segment has **177 CODE bytes**, including an executable
far unwind thunk, compiler exception descriptor and two complete far
reference/deletion helper functions. The `_TEXTC` segment has **254 bytes**:
a complete 54-byte public method and three typed C++ RTTI descriptors for
`string::outofrange` (+54), `xalloc` (+132), and `xmsg` (+198).
DATA and BSS are empty.

All **431 original CODE bytes**, the far public identity, all six original
imports, original code segment geometry, group `0aff02ff03` and **19
complete original FIXUPPs match literally in original record order**, with
all frames, targets, widths and addends. The real 8086 instructions and
typed RTTI structures are authored using symbolic source at genuine
original `ORG` offsets; no executable byte arrays, binary patches or
synthetic padding are used. Full Borland OMF member record serialization
still differs in unrelated metadata and is not claimed equal.

`scripts/build_th03_mainl_after374_work.py string-reserve-capacity-boss`
revalidates the **459-source** Japanese CRT parent and compiles this entire
changed original member before reconstructing all **893 original CL.LIB
slots** and running two independent native TASM/TLIB/TLINK rounds. Both
produce the original decoded **67,372-byte Japanese MAINL EXE and full MAP
byte-for-byte**, including all **677 ordered DOS MZ relocations**. The
working-source CRT reaches **460 complete original-equal members** and
**433 untouched contextual original programs**, totaling **146,094
original-equal source CODE bytes**, an increase of **431**. Native raw
OBJ/LIB/EXE/MAP, writer logs and parent/source SHA proofs are retained
under `.analysis/work/after374-*`; the independent reviewer and OMF/MZ
tests are `scripts/review_th03_mainl_after374_work.py` and
`tests/test_mainl_after374_work.py`.

This establishes scoped working CRT source, not formal Factory-accepted
decoded extent or canonical packed-file unit credit; no cold replay ran.
