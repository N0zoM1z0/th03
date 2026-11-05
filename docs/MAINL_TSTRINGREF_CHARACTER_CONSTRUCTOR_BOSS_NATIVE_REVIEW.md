# Complete TStringRef(char, capacity) constructor — after480

The original Japanese CL.LIB member ctor8 (index 396) is now
maintained in [8086 source](../src/mainl/crt/ctor8.asm).
This fully reconstructs the **197-byte FAR C++ constructor**.
The optional 12-byte object allocation, reference count,
rounded capacity through TStringRef::round_capacity, malloc
of the capacity-plus-terminator buffer, genuine memset
initialization with its original 16-bit char argument, final
far NUL-termination and global destructor counter are restored.
If malloc returns zero, the exact original xalloc address
is passed to the actual far xalloc::raise, preserving the
original unchecked behavior rather than adding a defensive exit.

All 197 CODE bytes and seven complete logical OMF FIXUPPs
match the original, including CODE+18 far new, +62 capacity
rounding, +81 malloc, +109 xalloc address, +113 raise,
+140 memset and +170 reference destructor count.
An initial source hypothesis used a read of the xalloc
word; the original B8h opcode proves that the **address**
of xalloc must instead be passed. The exact CODE comparison
detected and corrected this before integrating the build.
The original GROUP is DATA-before-BSS (08ff02ff03);
TASM initially emitted the reverse when given the same
group declaration text. Reversing the source group syntax
restored the original GROUP record without relaxed checking.
Original literal Borland/TASM FIXUPP chronology remains
different and raw original vendor OBJ identity is not claimed.

After480 checks the retained after479 687-source parent and
runs two fresh native TASM/TLIB/TLINK rounds, retaining
raw OBJ/LIB/EXE/MAP vectors, full writer logs, source and
driver hashes. Both decoded Japanese MAINL EXE and MAP
match the original targets byte-for-byte: 67,372-byte EXE
and 677 ordered MZ relocations. Working CRT:
**688/893 source-linked original members**,
**183,350 source CODE bytes**, 205 contextual vendor objects.
This is bounded source-build evidence, not a full cold replay
or new Factory accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after480_work.py
(mode tstringref-character-capacity-constructor-boss).
Tests: tests.test_mainl_after480_work.
