# Original istream double x87 overflow check and FAR assignment — after517

Japanese Borland CL.LIB member istedbl (original slot 762) is now
recovered as [maintained 8086/x87 source](../src/mainl/crt/istedbl.asm).
Its complete 124-byte FAR istream double extraction operator calls the
actual ten-byte long-double extractor, checks the original ios
stream error bits, compares against both signs of Borland
__huge_dble, raises ERANGE via the real _errno state on
range failure, and stores the original rounded FAR double result
with x87 fstp. Native FPU emulator instructions and caller
stack ABI are preserved.

**All 124 original CODE bytes** and 18 logical OMF fixup
sites, original symbolic import identities, kinds, widths and
addends match. A first source attempt emitted six bytes too few:
Borland EMUL needs three explicit fwait directives after the
two FPU status stores and final double store. The first range
error branch must land on the final FPU wait sequence, not after
it. Both details were corrected from original byte evidence.
Fourteen original Borland x87 references use frame method 4
where TASM emits method 5; this is explicitly verified and
is *not* literal original raw OBJ identity. TASM may repeat
its FPU EMUL extern declarations; imports are compared by
original symbolic identity, never by accidentally equal
numeric EXTDEF indices.

after517 independently verifies the unchanged after516
**724-source** carrier and creates two real TASM/TLIB/TLINK
native output rounds. Both complete Japanese decoded
MAINL EXE/MAP equal the pinned original files byte-for-byte
(67,372 EXE bytes, 677 ordered MZ relocations).
Raw OBJ/LIB/EXE/MAP outputs, writer logs, source/driver
hashes and parent receipt are protected. Working CRT:
**725/893** complete source-linked members,
**193,939 original-equal CODE bytes**; 168 contextual
vendor members remain. This is working-source evidence,
not full cold replay or Factory canonical accepted credit.

Independent reviewer: scripts/review_th03_mainl_after517_work.py
(mode istream-double-bounds-x87-wrapper).
Tests: tests.test_mainl_after517_work.
