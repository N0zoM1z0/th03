# Original DOS create/new-create with native FAR output handle — after513

The Japanese Borland CL.LIB member doscreat (index 23) is
fully recovered as maintained [8086 source](../src/mainl/crt/doscreat.asm).
It includes the complete private near DOS 21h file creation
engine at CODE+0..39 and two real FAR public interfaces:
__dos_creat at CODE+40 and __dos_creatnew at CODE+70.
The private helper preserves DS while invoking actual DOS
INT 21h, writes the resulting handle through a caller's
FAR output pointer and returns zero on success. On failure,
it invokes the genuine near __DOSERROR handler. The two FAR
interfaces select AH=3Ch (create) or AH=5Bh (new-create)
with the original word attributes and stack convention.

All **100 original CODE bytes**, two public offsets, sole
__DOSERROR import, empty DATA/BSS and DATA-before-BSS
group match the original Borland member. Its sole **literal
ordered original OMF FIXUPP** at CODE+32 matches the native
near error call exactly, including target/frame/width/addend.
The source contains no target opcode arrays, filler or
post-assembly OMF/EXE rewriting.

After513 verifies the preserved after512 720-source parent
and runs two independent native TASM/TLIB/TLINK rounds.
Both complete decoded Japanese MAINL EXE/MAP match their
pinned originals byte-for-byte (67,372 EXE bytes,
677 ordered DOS MZ relocations). Both raw OBJ/LIB/EXE/MAP
vectors, writer logs, source/driver hashes and parent
receipt remain protected. Working CRT reaches **721/893**
complete original source-linked members, **187,986 CODE
bytes**, with 172 contextual vendor members.
This is scoped working-source parity, not full cold replay
or formal Factory source acceptance.

Reviewer: scripts/review_th03_mainl_after513_work.py,
mode dos-create-newcreate-two-far-apis.
Tests: tests.test_mainl_after513_work.
