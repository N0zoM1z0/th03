# Original Borland DOS open and rtl_open with native descriptor flags — after511

The original Japanese CL.LIB member opena (slot **268**) is now
maintained in [8086 source](../src/mainl/crt/opena.asm).
It contains two complete FAR APIs: __rtl_open at CODE+0
and __open at CODE+83. The former translates the actual
Borland access/mode flags into DOS AH=3Dh/AL flags, uses
the caller's genuine FAR DS:DX pathname, and invokes
native INT 21h. It records the original __openfd state
when successful, or passes the actual DOS error to near
__IOERROR. The __open wrapper uses the exact 16-bit
PUSH CS and same-CODE near call convention.

All **108 original CODE bytes**, original public names/offsets,
two ordered imports, empty DATA/BSS, DATA-before-BSS
GROUP, and both **literal ordered original OMF FIXUPPs**
match Japanese CL.LIB, including CODE+66 __openfd and
CODE+75 __IOERROR. There are no target-code fixtures,
padding, original OBJ mutations or host OS replacements.

After511 independently validates the retained after510
**718-source** working CRT parent, then performs two fresh
TASM/TLIB/TLINK native rounds. Both decoded Japanese
MAINL EXE and MAP exactly match their pinned originals,
including the 67,372-byte EXE and 677 ordered MZ relocations.
Complete raw OBJ/LIB/EXE/MAP pairs, writer logs, source and
driver hashes, and the parent receipt are preserved.
Working CRT advances to **719/893** source-linked original
members, **187,734 CODE bytes**, with 174 contextual
vendor members. No full cold replay or formal Factory
source acceptance is claimed.

Reviewer: scripts/review_th03_mainl_after511_work.py,
mode dos-rtl-open-file-handle-flags.
Tests: tests.test_mainl_after511_work.
