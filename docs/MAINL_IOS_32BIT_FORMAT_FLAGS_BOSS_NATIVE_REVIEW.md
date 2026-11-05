# Original ios::setf(long) and three mutually exclusive fmtflag groups — after483

Original Japanese Borland CL.LIB member stsetf1 (slot **882**) is
maintained as natural [8086 source](../src/mainl/crt/stsetf1.asm).
It is the entire original **195-byte FAR ios::setf(long flags)**
method. The routine saves the previous two-word format flags,
tests the 32-bit input flags against each of the original three
global format-field masks, and conditionally clears the old
mask family before setting the requested flags. It implements
the real @ios@adjustfield, @ios@basefield and @ios@floatfield
mutual exclusivity, and updates the original ios state word
with the high-level 0100h bit implied by low fmtflag bit 0.
The original FAR pointer and 32-bit return ABI are preserved.

The complete 195 CODE bytes match Japanese CL.LIB. Its entire
twelve original logical OMF relocations also match at their
original offset/width/frame/target/addend fields: CODE+33/+37/
+45/+48 for adjustfield, +70/+74/+82/+85 for basefield, and
+110/+114/+122/+125 for floatfield, with their real high-word
addends +2. The original _TEXTA/_DATA/_BSS segment layout,
DATA-first GROUP, public name, three ordered imports and empty
DATA/BSS also agree. Borland and TASM literal FIXUPP chronology
differs; full raw original OBJ equality is not asserted and the
implementation does not rely on copied executable bytes.

After483 checks the unchanged after482 690-member carrier before
two independent native TASM/TLIB/TLINK rounds; both decoded
Japanese MAINL EXE and MAP are byte-for-byte target-equal,
preserving 67,372 EXE bytes and 677 ordered MZ relocations.
All raw OBJ/LIB/EXE/MAP outputs, logs and source/driver hashes
are retained. The working CRT reaches **691/893 original
source-linked members and 183,932 CODE bytes**, with 202
contextual vendor members remaining. This is not a full
cold replay or Factory accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after483_work.py,
mode ios-32bit-format-flags-boss; tests:
tests.test_mainl_after483_work.
