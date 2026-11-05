# Original DOS chsize growth, zero-fill, truncation and seek boss — after475

The original Japanese Borland CL.LIB chsize member (index **203**)
is now recovered as maintainable
[8086 source](../src/mainl/crt/chsize.asm).
This is the entire **199-byte** FAR _chsize function, not
a thin DOS seek call. It gets and saves the original 32-bit DOS
file offset through INT 21h AX=4201h, queries the old EOF
(AX=4202h), then uses AX=4200h and AH=40h to either truncate
or **extend the real file with original zero-filled 128-byte
buffer blocks**. It restores the original file position,
marks the original per-descriptor flags and propagates real
DOS errors via the imported near __IOERROR.

All 199 CODE bytes are original-equal, including the genuine
132-byte temporary stack frame and one-byte branch displacement
at CODE+133. The first source hypothesis jumped to the loop
condition rather than back to the MOV CX,80h block-size reset;
original CODE comparison caught this, and the label was corrected.
Both **literal ordered original OMF FIXUPPs** also match
exactly: CODE+138 __IOERROR with CODE frame, and CODE+187
__openfd with its DGROUP frame. Original three-segment
layout, BSS-before-DATA GROUP, FAR public and imports match.
There are no target-byte CODE arrays or OBJ mutations.

After475 checks the untouched after474 682-source native carrier,
then executes two fresh real TASM/TLIB/TLINK native rounds
preserving raw OBJ/LIB/EXE/MAP pairs, source/driver hashes and
writer logs. Both complete decoded Japanese MAINL EXE/MAP are
byte-for-byte original-equal (67,372-byte EXE, 677 ordered DOS
MZ relocations). The working CRT reaches **683/893 source-linked
original members, 182,479 CODE bytes**, with 210 remaining
contextual vendor objects. This is scoped working-source parity,
not new Factory acceptance or full cold replay.

Focused reviewer: scripts/review_th03_mainl_after475_work.py,
mode dos-file-chsize-grow-truncate-boss;
tests: tests.test_mainl_after475_work.
