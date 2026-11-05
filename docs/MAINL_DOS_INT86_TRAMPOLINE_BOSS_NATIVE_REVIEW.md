# Complete original DOS int86 / int86x register and interrupt trampoline — after471

Original Borland CL.LIB int86 member (index **175**) is maintained
as [native 8086 source](../src/mainl/crt/int86.asm). Both complete
FAR exported functions are recovered, _int86 (CODE+0) and _int86x
(CODE+53). The former fetches the true segment register image
through _segread and delegates to the common dynamic bridge;
the latter builds the authentic inline 16-bit INT nn opcode and
FAR epilogue in its own stack memory, with special original
handling of interrupts 25h and 26h.

The code loads caller-supplied AX/BX/CX/DX/SI/DI and segment registers,
invokes the stack-resident FAR trampoline, captures FLAGS twice,
restores the original registers and output segment-state data,
tests the native carry/error flag and conditionally invokes
__IOERROR. Every 16-bit stack offset, near/far call convention,
original PSP/segment behavior and fallback epilogue are preserved.

All **207 original CODE bytes**, zero DATA/BSS, two exact FAR PUBLIC
offsets, imports and the BSS-before-DATA GROUP 08ff03ff02 match.
Both **literal ordered original OMF FIXUPPs** are identical:
CODE+14 FAR _segread and CODE+198 imported near __IOERROR,
with exact frame/target semantics and original addends. Strict
source comparison exposed an initial group declaration mismatch;
this was repaired in the 8086 source without accepting a
nonoriginal native group. No patched CODE bytes or original-byte
arrays were used.

After471 verifies the unchanged after470 678-source CRT carrier,
then builds twice with native TASM/TLIB/TLINK and retains full
raw OBJ/LIB/EXE/MAP pairs, source hashes and writer logs.
Both complete decoded Japanese MAINL EXE and MAP match their
original targets: 67,372 EXE bytes, 677 ordered MZ relocations.
The working CRT is now **679/893** original source-linked
members and **181,827 original-equal CODE bytes**, leaving
214 contextual vendor members. This is bounded source evidence,
not new Factory acceptance or a full cold replay.

Focused reviewer: scripts/review_th03_mainl_after471_work.py
(mode dos-int86-int86x-register-boss);
tests: tests.test_mainl_after471_work.
