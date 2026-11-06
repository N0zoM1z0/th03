# Original FAR strncat with native far strlen and memory move — after509

The original Japanese Borland CL.LIB member fstrncat (index 449)
is fully maintained as [8086 source](../src/mainl/crt/fstrncat.asm).
Its complete FAR __fstrncat obtains both original FAR string
lengths through the authentic __fstrlen, caps the appended length
to the requested word count, computes the original 16-bit FAR
destination offset, calls the true __fmovmem to copy the bytes,
and writes the trailing NUL to the actual destination segment.
It returns the caller's original DX:AX FAR destination pointer.
There are no host string abstractions or forward-only memcpy
substitutes.

All **105 original CODE bytes**, one FAR public, two genuine
ordered imports, empty DATA/BSS and original DATA-first GROUP
match. All three logical OMF FIXUPP locations, widths, frames,
targets and addends match at CODE+15/+31 to __fstrlen and
+71 to __fmovmem. The original Borland literal FIXUPP
chronology differs from native TASM, so raw original vendor
OBJ identity is not claimed. No copied opcode arrays,
arbitrary padding or post-assembly patches were introduced.

After509 checks its unchanged after508 **716-source** CRT parent,
then runs two fresh TASM/TLIB/TLINK rounds retaining the complete
native OBJ/LIB/EXE/MAP vectors, writer logs and source/driver
hashes. Both decoded Japanese MAINL EXE/MAP match the pinned
originals byte-for-byte (67,372 EXE bytes, 677 ordered MZ
relocations). Working CRT advances to **717/893 complete
source-linked original members**, **187,517 original-equal CODE
bytes**, with 176 contextual original vendor members.
This remains scoped working-source parity, not full cold replay
or new Factory source acceptance.

Focused reviewer: scripts/review_th03_mainl_after509_work.py,
mode original-far-strncat-move-leaf.
Tests: tests.test_mainl_after509_work.
