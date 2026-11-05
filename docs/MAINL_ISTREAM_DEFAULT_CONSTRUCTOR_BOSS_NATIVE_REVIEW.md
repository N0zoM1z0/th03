# Original istream() default constructor and ios base — after444

The Japanese Borland CL.LIB member istctr1 (index **751**) is
fully reconstructed as maintained [8086 source](../src/mainl/crt/istctr1.asm).
The full C++ constructor conditionally allocates a **46-byte** object,
creates its embedded ios base at +6 unless passed an initialized
base, assigns **two distinct vtable pointers**, initializes the original
status field, and increments the 32-bit destructor reference counter.
The original near/far this-adjusted destruction thunk changes this
by -6 before jumping to the real istream destructor.

The source produces the entire original **254 CODE + 20 initialized
DATA bytes**, with two genuine Borland typed RTTI descriptors
(istream at CODE+134 and ios), the destructor thunk at CODE+122,
the original DATA+8 virtual pointer and DATA+16 adjusting thunk.
All **12 original logical OMF relocations** match exact sites,
widths, frame/target methods and addends. The original Borland and
TASM **literal FIXUPP ordering differs**; full member record equality
is not claimed. No copied CODE byte arrays or post-assembly patches.

After444 independently verified the existing after443 651-member
source-bound parent and produced two fresh native TASM/TLIB/TLINK
rounds. Both complete Japanese decoded MAINL EXE and MAP match the
original, preserving 67,372 EXE bytes and 677 ordered MZ relocations.
The working CRT is **652/893** original source-linked members and
**175,770 original-equal CODE bytes**, with 241 vendor members still
contextual. This is source-bound working evidence, *not* Factory
formal accepted-source credit or a full cold replay.

Focused reviewer: scripts/review_th03_mainl_after444_work.py
(mode istream-default-constructor-boss);
unit tests: tests.test_mainl_after444_work.
