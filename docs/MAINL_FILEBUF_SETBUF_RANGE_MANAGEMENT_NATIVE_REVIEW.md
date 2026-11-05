# Complete filebuf::setbuf buffer management — after452

Japanese Borland original member fsbsbuf (CL.LIB index 714) is now
recovered as real 8086 [source](../src/mainl/crt/fsbsbuf.asm).
The complete far `filebuf::setbuf(char far*, int)` first refuses to
replace a live attached buffer. For a valid incoming far pointer and
positive length it uses the original 8-byte threshold to reserve
one or four bytes of buffer control; otherwise it clears the incoming
far pointer/length state, without adding safety checks absent from
its original. It calls the actual `streambuf::setb`, `setp` and `setg`
methods with their original FAR pointer widths, precisely preserving
the offset-only arithmetic, all copied 16-bit stack arguments, and
the final 42-byte stack cleanup.

Full original **191 CODE bytes** match. All three logical original
OMF fixups agree at every site, target, frame and width:
CODE+110 -> `setb` (import 3), CODE+138 -> `setp` (import 1),
CODE+172 -> `setg` (import 2). The native segment/GROUP layout,
public, ordered imports and empty DATA/BSS also agree. Borland's
literal FIXUPP record chronology remains different from TASM's;
raw OBJ program equality is not asserted and there are no output
patches or target-byte CODE fixtures.

After452 verifies the 659-source after451 parent receipt then runs
two independent TASM/TLIB/TLINK rounds with full source hashes,
writer logs, and raw OBJ/LIB/EXE/MAP pairs preserved. Both complete
Japanese decoded MAINL EXE and MAP match the target including
67,372 EXE bytes / 677 original ordered MZ relocations. The working
CRT now contains **660/893** original source-linked members,
**177,498 original-equal CODE bytes**, and 233 unchanged contextual
vendor members. These remain working-source results, not formal
Factory acceptance or a full cold replay.

Focused reviewer: scripts/review_th03_mainl_after452_work.py,
mode filebuf-setbuf-range-management; tests: tests.test_mainl_after452_work.
