# Original segmented FAR calloc with 32-bit length and chunked clearing — after515

Original Japanese Borland CL.LIB member fcalloc (slot 168) is now
fully maintained in [natural 8086 source](../src/mainl/crt/fcalloc.asm).
It uses the true near N_LXMUL@ to multiply two 32-bit count/element
arguments, allocates through the real FAR _farmalloc helper, then
zeroes allocated memory using FAR _setmem. The original algorithm
iterates over 16-bit chunks capped at 0xFA00 bytes and advances
its segmented address through genuine near N_PADA@. It preserves
all original unchecked allocation behavior and caller/register ABI.
No replacement host allocator or platform memset was introduced.

The complete **148 original CODE bytes**, FAR public _farcalloc
at CODE+0, four original imports, original DATA/BSS layout and
GROUP match the pinned Japanese library. **All four original
literal ordered OMF FIXUPPs** match at CODE+21 (N_LXMUL@),
+32 (_farmalloc), +98 (_setmem) and +116 (N_PADA@), including
every original site, width, frame and symbolic target. No target
machine-byte fixtures, padding or OBJ modifications were used.

after515 independently validates the retained after514 722-source
full cplx2 carrier and performs two new TASM/TLIB/TLINK native rounds
while preserving both complete OBJ/LIB/EXE/MAP vectors and writer
logs. Both complete decoded Japanese MAINL EXE and MAP exactly match
their originals, including 67,372 EXE bytes and 677 ordered MZ
relocations. Working CRT now counts **723/893** original complete
source-linked members, **193,732 CODE bytes**, and 170 contextual
vendor members. Neither a full cold replay nor formal Factory
canonical source acceptance is claimed.

Reviewer: scripts/review_th03_mainl_after515_work.py
(mode farcalloc-32bit-segmented-zeroing-boss).
Tests: tests.test_mainl_after515_work.
