# Original Borland srand/rand 32-bit LCG — after495

Japanese CL.LIB member rand (slot **102**) is fully maintained in
[8086 source](../src/mainl/crt/rand.asm). It exports two FAR
routines: _srand at CODE+0 and _rand at CODE+21. It preserves
the true 4-byte initialized state (seed=1), resets both 16-bit
halves in srand and advances the original generator using
the N_LXMUL@ 32-bit near multiply with constant 015A4E35h,
adds one and returns the upper 15 bits of the new state.
No host-side RNG is substituted.

All **62 original CODE bytes**, the four typed initialized DATA
bytes, two FAR publics and eight genuine logical OMF fields
match their original meanings. Seven relocation fields match
completely; the only difference is the near imported N_LXMUL@
call at CODE+38: Borland uses target frame method 5 and TASM
uses equivalent CODE frame method 0. This exact site/import is
locked by the producer and test. Original literal FIXUPP
chronology and full raw Borland OBJ identity are not claimed.

After495 verifies the retained after494 **702-source** CRT parent
before two new TASM/TLIB/TLINK rounds, preserving OBJ/LIB/EXE/MAP
vectors, writer logs, source/driver hashes and parent evidence.
Both decoded Japanese MAINL EXE and MAP exactly match the pinned
originals (67,372 bytes; 677 ordered MZ relocations).
Working CRT: **703/893** original source members,
**185,749 source CODE bytes**, 190 vendor-context members.
No cold replay or new formal Factory credit is claimed.

Focused reviewer: scripts/review_th03_mainl_after495_work.py,
mode original-srand-rand-lcg-leaf. Test: tests.test_mainl_after495_work.
