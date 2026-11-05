# Original stdio getw two-byte buffer leaf — after468

Japanese Borland CL.LIB member getw (index **66**) is maintained
as [natural 8086 source](../src/mainl/crt/getw.asm).
The complete FAR _getw(FILE far*) routine retrieves the low and high
bytes independently, first taking the original FILE buffer-level
and cursor fast path and otherwise falling back to the real far
__fgetc. It preserves both original EOF(-1) paths, the native
little-endian word composition, the original FAR FILE access
and the compiler's local two-word stack frame. There are
no defensive shortcuts or high-level substitute reads.

All **130 original CODE bytes**, no DATA/BSS, the original single
FAR public, ordered __fgetc import, complete segments and group,
and both logical original OMF relocation fields match. The two
far fgetc calls are at CODE+44 and CODE+94; their original
Borland versus TASM FIXUPP record order differs. Full raw vendor
OBJ equality is not claimed and no post-assembly patches occur.

The first new stage's strict inherited-native gate caught a
new-source generator mistake: the after468 carrier had correctly
advanced from 674 to 675 source members, but its stored
contextual-vendor counter was still 219 instead of 218. This
was repaired as an exact parent-count constraint, rather than
bypassing source membership checking. The ignored local helper
was changed to perform field-anchored count replacements rather
than broad number substitutions.

After468 validates the unchanged after467 source-bound receipt,
then performs two new TASM/TLIB/TLINK rounds and retains all
OBJ/LIB/EXE/MAP vectors, logs and source hashes. Both complete
Japanese decoded MAINL EXEs and MAPs are original-equal
(67,372 bytes, 677 ordered MZ relocations). The working CRT now
contains **676/893 original source-linked members** and
**181,204 source CODE bytes**, with 217 contextual vendor members.
This is not full cold replay or Factory source acceptance.

Focused reviewer: scripts/review_th03_mainl_after468_work.py
(mode stdio-getw-two-byte-leaf);
tests: tests.test_mainl_after468_work.
