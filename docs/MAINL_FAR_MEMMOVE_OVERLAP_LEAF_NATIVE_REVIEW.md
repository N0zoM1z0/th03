# Original overlap-safe FAR memmove and wrapper leaf — after479

Original Japanese Borland CL.LIB member fmovmem (index **439**)
is now fully maintained as natural [8086 source](../src/mainl/crt/fmovmem.asm).
It provides two original FAR interfaces: __fmovmem at CODE+0
and __fmemmove at CODE+82.

The actual memory copy compares the original two FAR pointers
through near Borland N_PCMP@, chooses STD for backward overlapping
copies or CLD for forward copies, restores DS/ES from the original
FAR arguments, aligns the destination word address if needed,
uses the native REP MOVSW bulk copy and trailing MOVSB byte,
and always restores the direction flag before return. The
wrapper makes the exact original PUSH CS plus same-CODE NEAR
call into the first entrypoint, restores stack arguments and
returns the original FAR destination pointer. This is not a
high-level forward-only memcpy approximation.

All **119 original CODE bytes**, zero DATA/BSS, two FAR
publics, original BSS-before-DATA GROUP and sole ordered
N_PCMP@ import match. Its single **literal ordered original OMF
FIXUPP** is exactly the CODE-frame method 0 near N_PCMP@
call at CODE+19, including original target, addend and width.
No target opcode fixtures, filler bytes, or post-assembly
object rewriting occur.

After479 verifies the entire retained after478 686-source
native parent then runs two fresh TASM/TLIB/TLINK rounds,
preserving all original OBJ/LIB/EXE/MAP pairs, writer
logs, and source/driver hashes. Both full Japanese
decoded MAINL EXE and MAP are byte-for-byte original-equal
(67,372 EXE bytes and 677 ordered MZ relocations).
Working CRT: **687/893** source-linked original members,
**183,153 original-equal CODE bytes**, 206 contextual vendor
members. This remains source-bound working parity, not new
Factory acceptance or a full cold replay.

Focused reviewer: scripts/review_th03_mainl_after479_work.py
(mode far-overlap-safe-memmove-leaf).
Tests: tests.test_mainl_after479_work.
