# Complete complex double-precision x87 arithmetic boss — after461

Japanese original Borland CL.LIB cplx1 (slot **208**) is recovered
in maintained [8086/x87 source](../src/mainl/crt/cplx1.asm).
Its four native FAR exports are abs(complex) (CODE+0),
norm(complex) (+46), complex::operator*= (+89), and the
return-object operator* (+167), including the real FAR allocation
of the 16-byte complex result when the hidden output pointer is null.
This is the complete original arithmetic with x87 floating-point stack
sequencing, separate real/imaginary products, local double and
80-bit extended temporaries, and the original C++ return ABI.

All **364 CODE bytes** reproduce the original Japanese Borland
library member, with zero DATA/BSS, original _TEXT segment,
BSS-before-DATA GROUP, and all four original PUBLIC entries.
All **55 original logical OMF relocation fields** match the true
site, width, method, frame, target and addend, including all
FIERQQ/FIDRQQ/FIWRQQ emulated x87 references and the FAR
@$bnew$qui allocation site at CODE+309. Native TASM5 EMUL
is used with genuine x87 arithmetic rather than handcrafted CODE bytes.

An important Borland/TASM source-scope trap was resolved, not hidden:
declaring @$bnew$qui inside the middle of the active _TEXT segment
made TASM emit an invalid PUSH CS; CALL near, even with a FAR call
qualifier, and produced 363 CODE bytes plus a wrong near OMF FIXUPP.
Moving the FAR external declaration outside the active _TEXT
restored the original true 9Ah FAR call. However declaring it before
the first emitted FIWRQQ reference gave the wrong ordered import ABI.
The source now briefly closes/reopens **the very same _TEXT
segment** after the first natural FIWRQQ-emitting fwait instruction,
then declares the FAR allocator outside the segment before its use.
This preserves a single original 364-byte CODE segment, the genuine
import order FIERQQ,FIDRQQ,FIWRQQ,@$bnew$qui, and the true FAR
call plus all 55 fixups. The fourth function has a normal FAR label
around the segment boundary. No target-byte arrays, object mutations
or padding are used.

The original Borland/TASM **literal ordered FIXUPP record sequence**
still differs; full original raw OBJ program identity is not claimed.
After461 checks the inherited after460 668-source parent and runs
two fresh native TASM/TLIB/TLINK rounds. Both decoded Japanese
MAINL EXE and MAP match original files byte-for-byte, including
the 67,372-byte EXE and all 677 ordered MZ relocations. Raw two-round
OBJ/LIB/EXE/MAP, writer logs, and source hashes are retained.
Working CRT now covers **669/893 original source-built members**,
**179,780 CODE bytes**, and 224 remaining contextual vendor members.
No full cold replay or new formal Factory source acceptance is implied.

Focused reviewer: scripts/review_th03_mainl_after461_work.py
(mode complex-x87-multiply-boss).
Tests: tests.test_mainl_after461_work.
