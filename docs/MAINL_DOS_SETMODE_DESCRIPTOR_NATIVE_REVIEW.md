# Original Borland DOS setmode descriptor flag leaf — after516

Japanese Borland CL.LIB setmode (slot 284) is now fully
reconstructed as maintained [8086 source](../src/mainl/crt/setmode.asm).
The complete FAR _setmode validates the caller's file descriptor
against native __nfile, validates the requested text/binary mask
against Borland 0xC000 bits, updates the true __openfd state,
returns original old mode bits and reports original DOS errors
through near __IOERROR.

All **83 original CODE bytes**, sole public FAR name, ordered
__nfile/__IOERROR/__openfd imports, four genuine logical OMF
fixups, segment definitions and BSS-before-DATA GROUP agree with
the original CL.LIB member. Three literal symbolic relocations
at CODE+13/+47/+63 match completely. The original imported
near __IOERROR call at CODE+77 has Borland target-frame method
5, while TASM emits CODE-frame method 0 with the same original
target, location width and addend. This **exact one-site
difference** is checked rather than globally normalized or
misrepresented as literal original OMF identity. No target-code
arrays, artificial padding or OBJ rewriting were used.

after516 verifies its unchanged after515 **723-source** parent
and performs two fresh TASM/TLIB/TLINK native rounds with full
OBJ/LIB/EXE/MAP vectors, logs and source/driver hashes retained.
Both decoded Japanese MAINL EXE/MAP are original-equal, including
67,372 EXE bytes and 677 ordered MZ relocations. Working CRT
now **724/893** complete source-linked original members,
**193,815 original CODE bytes** and 169 contextual vendor members.
This is working-source parity, not a cold replay or formal
Factory canonical source acceptance.

Reviewer: scripts/review_th03_mainl_after516_work.py
(mode dos-file-descriptor-mode-switch-leaf).
Tests: tests.test_mainl_after516_work.
