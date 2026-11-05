# Original CRT exit/atexit lifecycle and symbolic callback order — after494

The Japanese Borland CL.LIB exit member (slot 42) is now
recovered as native [8086 source](../src/mainl/crt/exit.asm).
It contains the private FAR no-op handler at CODE+0, the
complete original near process shutdown engine at CODE+5,
and four full FAR public exit interfaces: _exit (CODE+95),
__exit (+114), __cexit (+136), and __c_exit (+154).
The actual shutdown engine decrements the true atexit
count, invokes the real LIFO FAR callback table, calls
the original cleanup/restore/check routines and
conditionally invokes the original DOS termination
interface with the caller's original 16-bit exit status.

**All 170 CODE and 12 DATA bytes**, the original four
public CODE entries, three DATA-public FAR handler slots,
six ordered imports and 14 logical OMF relocation fields
match Japanese CL.LIB. The twelve DATA bytes are not padding:
they are three independently mutable original FAR pointers
to the real CODE+0 no-op handler:
__exitbuf at DATA+0, __exitfopen at DATA+4, and
__exitopen at DATA+8.

The first native implementation had exact CODE/DATA
and all 14 logical OMF fields but failed the **full
EXE equality** gate. An independently preserved failing
linked.exe showed exactly two changed relocation-table
bytes: the original MZ relocation ordering at indices
465 and 467 was swapped while MAP was otherwise
identical. The root cause was Borland's **reverse
DATA FIXUPP chronology (8,4,0)** for the three callback
pointers. TASM initially emitted them in ascending order
(0,4,8). The source now uses meaningful symbolic
FAR callback definitions with source-level descending
ORG 8/4/0, rather than executable byte fixtures or
post-assembly OMF editing. The resulting native
DATA FIXUPP order matches the original and **both full
MAINL EXE/MAP rounds now match the target byte-for-byte**,
including original ordered MZ relocations.

The complete raw Borland OBJ record sequence is not
identical: original DATA LEDATA is one 12-byte record;
native TASM emits three four-byte records in descending
offset order, and the full CODE fixup serialization
still differs. These limitations remain explicit; we
do not assert literal *all-member* FIXUPP chronology
or original raw OBJ identity.

After494 checks the complete unchanged after493
701-source CRT carrier, then runs two new TASM/TLIB/TLINK
rounds, retaining raw OBJ/LIB/EXE/MAP outputs and source/
driver/log hashes. Both full decoded Japanese MAINL
EXE/MAP are original-equal (67,372 bytes; 677 ordered
MZ relocations). Working CRT: **702/893** maintained
original source members, **185,687 CODE bytes**, and
191 contextual vendor programs. No full cold replay
or formal Factory source acceptance is claimed.

Focused reviewer: scripts/review_th03_mainl_after494_work.py
(mode crt-exit-atexit-lifecycle-boss).
Tests: tests.test_mainl_after494_work.
