# Original low-level DOS read core with two FAR exports — after502

Original Japanese Borland CL.LIB member reada (slot 103) is
now maintained in [8086 source](../src/mainl/crt/reada.asm).
It comprises the complete FAR __rtl_read at CODE+0 and
FAR __read at CODE+50. The actual native low-level routine
checks the original two-byte __openfd descriptor state,
performs genuine DOS INT 21h/AH=3Fh file reads with the
caller's FAR DS:DX buffer pointer, and passes real DOS
errors to near __IOERROR. The public __read wrapper
uses the original same-CODE PUSH CS plus near call into
__rtl_read with the original 16-bit argument ABI.

All **78 original CODE bytes**, both FAR public offsets,
two ordered imports, empty DATA/BSS and the original
BSS-before-DATA GROUP match. Both **literal ordered OMF
FIXUPPs** match exactly: CODE+12 for the descriptor
flag and CODE+44 for the near __IOERROR. This includes
original frame/target methods, widths and addends.
There are no target opcode arrays or object patches.

After502 checks the unchanged after501 **709-source**
carrier and builds two fresh TASM/TLIB/TLINK rounds
with all raw OBJ/LIB/EXE/MAP outputs and writer logs
preserved. Both full decoded Japanese MAINL EXE and MAP
are original-equal byte-for-byte (67,372 EXE bytes and
677 ordered MZ relocations). Working CRT reaches
**710/893** complete original source-linked members,
**186,653 source CODE bytes**, 183 contextual vendor
members. No full cold replay or formal Factory acceptance.

Focused reviewer: scripts/review_th03_mainl_after502_work.py
(mode dos-rtl-read-two-far-leaf).
Tests: tests.test_mainl_after502_work.
