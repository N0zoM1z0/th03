# Original 32-bit Borland srand/rand LCG with true seed data — after495

Japanese Borland CL.LIB member rand (slot 102) is now
maintained in [8086 source](../src/mainl/crt/rand.asm).
It contains two complete FAR APIs: _srand (CODE+0)
stores the caller's 16-bit seed into the true four-byte
state and zeros its high word; _rand (CODE+21)
performs the actual native 32-bit LCG step using
the real near N_LXMUL@ helper, multiplier 015A4E35h,
addend 1, then updates both seed halves and returns
the high 15 bits masked by 7FFFh.

All original **62 CODE and four DATA bytes** match.
The original DATA is a typed, mutable initialized
32-bit seed of 1, not padding. Both FAR entrypoints,
original group/segments, single ordered imported
multiply helper, and all **eight original logical
OMF relocations** agree in location, type, target,
width and addend. Seven OMF fields are identical.
The sole difference is the original Borland TARGET
frame method 5 versus TASM's CODE frame method 0
for the near N_LXMUL@ call at CODE+38.
This single site/import alternative is bounded and
independently tested, rather than a blanket exception.
Literal ordered original FIXUPPs and raw Borland OBJ
identity are not asserted.

After495 verifies the full retained after494
702-source CRT parent then runs two fresh native
TASM/TLIB/TLINK rounds retaining the original
source/driver hashes, both raw OBJ/LIB/EXE/MAP
vectors and all writer logs. Both Japanese decoded
MAINL EXE/MAP are byte-for-byte original-equal
(67,372 EXE bytes and 677 ordered MZ relocations).
Working CRT: **703/893** source-linked original
members, **185,749 CODE bytes**, 190 contextual
vendor programs. No full cold replay or formal
Factory source credit.

Focused reviewer: scripts/review_th03_mainl_after495_work.py
(mode original-srand-rand-lcg-leaf).
Tests: tests.test_mainl_after495_work.
