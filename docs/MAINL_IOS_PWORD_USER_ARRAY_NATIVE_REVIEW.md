# Original ios::pword user array access and conditional expansion — after505

The Japanese Borland CL.LIB member stpword (index 881) has
been recovered as natural [8086 source](../src/mainl/crt/stpword.asm).
Its complete FAR ios::pword(int) checks the original one-based
user index against the actual global ios::usercount, returns
a far pointer to real DATA+0 when invalid, otherwise
tests ios user-storage capacity at object+26h and calls
the original FAR ios::usersize(int) on demand. On success
it returns the computed four-byte FAR element address,
preserving the original unchecked pointer arithmetic.

All **97 CODE and four initialized DATA bytes** match the
original object. Its four real symbolic OMF references
also match target/frame/width/addend at CODE+12 (global
usercount), +22 and +68 (the genuine DATA invalid-slot
sentinel), and +46 (FAR usersize). Original _TEXTA/_DATA/_BSS,
DATA-first GROUP, one FAR public and two ordered imports
match. Borland and native TASM differ in literal FIXUPP
chronology, so raw vendor OBJ identity is not asserted.
There are no target-byte arrays or post-OBJ patches.

After505 validates the unchanged after504 **712-source**
CRT parent, then runs two real TASM/TLIB/TLINK rounds.
Both full Japanese MAINL EXE and MAP exactly match the
pinned originals (67,372 bytes and 677 ordered MZ
relocations). All raw OBJ/LIB/EXE/MAP vectors, logs,
source hashes and parent receipt are protected.
The working CRT reaches **713/893** source-linked members,
**187,043 CODE bytes**, 180 remaining vendor-context
members. This remains working-source parity, not formal
Factory acceptance or full cold replay.

Reviewer: scripts/review_th03_mainl_after505_work.py
(mode ios-pword-usersize-array-slot-boss).
Tests: tests.test_mainl_after505_work.
