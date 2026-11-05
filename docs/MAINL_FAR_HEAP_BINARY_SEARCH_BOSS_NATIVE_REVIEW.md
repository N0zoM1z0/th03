# Original FAR heap binary search with 32-bit pointer arithmetic — after489

Original Japanese Borland CL.LIB member hbsearch (slot **465**) is
recovered as [8086 source](../src/mainl/crt/hbsearch.asm).
The complete **145-byte** FAR __hbsearch routine maintains the
actual far low/high search pointers and unsigned element count,
calculates the midpoint through the real N_LXMUL@ 32-bit
multiply and N_PADD@ far pointer-add operations, invokes
the caller's true FAR comparator and then updates the
appropriate half of the search interval. It returns either
the actual matching FAR element pointer or a null FAR pointer;
the original 16-bit stack frame, signed comparison and
size/count arithmetic are retained.

All **145 original CODE bytes**, zero DATA/BSS, native segment/GROUP,
FAR public and two ordered imported near helper symbols match.
The original three imported-near OMF relocation sites, widths,
targets and addends at CODE+41 (N_LXMUL@), +54/+111
(N_PADD@) also match precisely. Borland expresses their
frames as target-frame method 5, while TASM uses CODE-frame
method 0; the scoped producer and independent test only allow
these three exact site/target/frame alternatives. Complete
literal FIXUPP identity and raw Borland OBJ identity are not
claimed. This source does not contain executable byte
fixtures, arbitrary padding or post-assembly patches.

After489 checks the full retained after488 696-source carrier,
then performs two fresh TASM/TLIB/TLINK rounds. Both
complete decoded Japanese MAINL EXE and MAP are original-
equal byte-for-byte (67,372-byte EXE, 677 ordered MZ
relocations). Both raw native OBJ/LIB/EXE/MAP vector
outputs, writer logs and source/driver hashes are retained.
The working CRT reaches **697/893** source-linked original
members, **184,835 CODE bytes**, with 196 contextual vendor
members. No full cold replay or new Factory source acceptance
credit is claimed.

Focused reviewer: scripts/review_th03_mainl_after489_work.py,
mode far-heap-binary-search-boss.
Tests: tests.test_mainl_after489_work.
