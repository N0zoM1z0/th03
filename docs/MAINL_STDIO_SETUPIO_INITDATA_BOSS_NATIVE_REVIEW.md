# Original Borland stdio startup with CRT INITDATA hook — after493

Japanese original CL.LIB member setupio (index 116) is now
maintained in natural [8086 source](../src/mainl/crt/setupio.asm).
Its complete __setupio near procedure initializes the
original Borland FILE/descriptor tables, handles the
inherited standard streams, chooses buffered/unbuffered
console modes using the real _isatty and _setvbuf FAR
callbacks, and installs correct native stream statuses.
It uses the original 16-bit loop/count/FILE stride ABI,
not host-side I/O substitutes.

The full **164 CODE bytes** match the original CL.LIB.
The fourth OMF segment _INIT_ of class INITDATA holds
six genuine bytes: priority 0200h, a symbolic CODE+0
address and one reserved word. The original BSS-before-
DATA GROUP and four SEGDEFs match exactly. All **18
original literal ordered OMF FIXUPPs** reproduce the
same segment, site, kind, frame, width, target, addend
and chronology, including INITDATA+2 -> CODE+0.

A key source-review finding prevented a subtle false
positive: the first code-byte-equal source candidate
used __openfd for six imported FILE-state operands.
Original Borland OMF FIXUPPs actually target __streams
at CODE+48/+64/+74/+105/+121/+131, even though the
unlinked CODE bytes are identical. The true file
status updates were corrected in source, while the
genuine __openfd descriptor initialization remains
at CODE+13. Original GROUP member order was also
recovered, not waived by the builder. No executable
target-byte fixture or OBJ mutation was introduced.

After493 validates the entire inherited after492
700-source carrier and produces two fresh
TASM/TLIB/TLINK native build rounds with full
raw OBJ/LIB/EXE/MAP outputs, logs, and
source/driver hashes retained. Both decoded Japanese
MAINL EXE/MAP match original targets byte-for-byte:
67,372 EXE bytes, 677 ordered MZ relocations.
Working CRT **701/893** original source-linked
members, **185,517 source CODE bytes**, 192 contextual
vendor members. This is not full cold replay or
formal Factory accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after493_work.py
(mode stdio-startup-stream-initdata-boss);
tests: tests.test_mainl_after493_work.
