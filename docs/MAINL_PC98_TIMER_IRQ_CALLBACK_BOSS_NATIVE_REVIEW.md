# Original PC-98 timer IRQ callback and FAR control boss — after477

The Japanese Borland CRT member pc98timr (CL.LIB index **508**) is
now recovered as meaningful [8086 ASM](../src/mainl/crt/pc98timr.asm).
The original private timer IRQ handler (CODE+0) saves the full
register/segment image, establishes its original DGROUP in DS,
fetches and atomically clears the prior four-byte FAR callback,
clears the one-byte busy flag, optionally invokes the FAR callback,
and restores all registers before the actual IRET. The public
_pc98timer FAR control entry at CODE+70 saves FLAGS, disables
interrupts for callback replacement, uses the genuine INT 1Ch
timer registration with ES:BX pointing to the private IRQ handler,
and optionally waits for the busy flag to clear.

All original **162 CODE + 5 initialized DATA bytes** match exactly.
All **13 logical OMF relocation fields** match, including the
segment-of-DGROUP reference at CODE+10 with original frame method
5 and GROUP target method 1, the CODE+127 handler offset and the
eleven real DATA cursor/flag fields. The first hypothesis
mistakenly generated a DATA-segment relocation for the initial
MOV BP,SEG instruction; using the actual SEG DGROUP construct
emitted the original GROUP relocation. The original polling
loop jumps to the status test, not to the preceding STI;
the original one-byte backward-branch displacement confirmed
and corrected the natural source label.

Original _TEXT/_DATA/_BSS segments, BSS-before-DATA group, public
ABI and zero external imports also match. The native TASM
FIXUPP packet chronology differs from original Borland,
and no raw original OBJ-program equality is asserted.
No target CODE arrays or post-assembly binary patches are used.

After477 checks the unchanged after476 684-source carrier
and runs two fresh native TASM/TLIB/TLINK rounds with complete
raw OBJ/LIB/EXE/MAP vectors, logs and source/driver hashes.
Both full Japanese decoded MAINL EXE/MAP equal the original
targets (67,372 EXE bytes, 677 ordered DOS MZ relocations).
The working CRT advances to **685/893** original source-linked
members and **182,846 source-built CODE bytes**, leaving
208 contextual vendor members. This remains scoped source
parity, not full cold replay or Factory accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after477_work.py
(mode pc98-timer-irq-callback-boss);
tests: tests.test_mainl_after477_work.
